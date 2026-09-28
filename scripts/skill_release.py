#!/usr/bin/env python3
"""Explicit-file Skill snapshots, candidate application, and reversible rollback.

Configuration: {"roots": [{"id": "repo", "root": "/absolute/root",
                          "paths": ["SKILL.md", "references/example.md"]}]}.
Paths are files, never globs. Snapshot paths may be absent. Candidate files must
exist; deliberate removals use top-level "delete": [{"root_id": "repo",
"path": "obsolete.md"}]. Candidate root IDs map to baseline target root IDs.

snapshot --config roots.json --output-dir BACKUP --temp-dir TEMP
verify --manifest BACKUP/manifest.json
apply --manifest BACKUP/manifest.json --candidate-config candidates.json
      --output-dir DEPLOYMENT --temp-dir TEMP [--apply]
restore --manifest BACKUP/manifest.json --deployment DEPLOYMENT/deployment.json
        --output-dir BEFORE_RESTORE --temp-dir TEMP [--apply]
capture --manifest BACKUP/manifest.json --config observed-roots.json
        --output-dir OBSERVED_EDITS --temp-dir TEMP [--apply]

Apply and restore default to dry-run. A restore snapshots current files first;
its own deployment.json allows that restore to be undone using the new snapshot.
Capture records already performed edits; --apply writes only the recovery record.
Unlisted additions require config "new_files": [{"root_id": "repo", "path":
"new.md"}]. This is an operator declaration, not proof of historical absence.
All manifests stay in the explicitly selected local output directory. No network
or credential discovery is performed. Hashes detect corruption, not authenticity.
PROJECT_STATE.json and its CURRENT_STATE projections can be snapshotted, but
application and rollback must update those through the project's state CAS API.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import sys
import tempfile
from datetime import datetime, timezone
import zipfile


class ReleaseError(ValueError):
    """Refused operation; no blanket force/overwrite bypass is available."""


SNAPSHOT_SCHEMA = "skill-release-snapshot/1"
DEPLOYMENT_SCHEMA = "skill-release-deployment/1"
BLOCKED_NAMES = {".git", ".ssh", ".aws", ".azure", "auth.json",
                 "credentials", "credentials.json", "credentials.toml",
                 "secrets.json", "secrets.yaml", "secrets.yml", "secrets.toml",
                 "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"}
BLOCKED_SUFFIXES = {".pem", ".key", ".p12", ".pfx"}
DEVICE_NAMES = {"con", "prn", "aux", "nul", *[f"com{x}" for x in range(1, 10)],
                *[f"lpt{x}" for x in range(1, 10)]}


def require(condition, message):
    if not condition:
        raise ReleaseError(message)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def sha_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_link(path):
    info = Path(path).lstat()
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & 0x400)


def check_name(name):
    lower = name.lower()
    require(lower not in BLOCKED_NAMES and not lower.startswith(".env"),
            "Credential or repository metadata path is prohibited")
    require(not re.fullmatch(r"\.?(?:secrets?|credentials|api[_-]?key|access[_-]?token|refresh[_-]?token)(?:\..*)?", lower),
            "Secret-bearing path name is prohibited")
    require(Path(name).suffix.lower() not in BLOCKED_SUFFIXES,
            "Private-key file type is prohibited")
    require(lower.split(".")[0] not in DEVICE_NAMES,
            "Reserved device path is prohibited")


def relative_path(value):
    require(isinstance(value, str) and value and "\x00" not in value,
            "A nonempty relative file path is required")
    value = value.replace("\\", "/")
    require(not value.startswith("/") and not PureWindowsPath(value).drive,
            "Absolute and drive-relative paths are prohibited")
    parts = value.split("/")
    for part in parts:
        require(part not in {"", ".", ".."} and not any(c in part for c in ':*?<>|"')
                and part == part.rstrip(" ."), "Unsafe relative path")
        check_name(part)
    return "/".join(parts)


def absolute_path(value, *, exists=False):
    path = Path(value)
    require(path.is_absolute(), "An explicit native absolute path is required")
    require(".." not in path.parts, "Parent traversal is prohibited")
    for component in reversed((path, *path.parents)):
        if component.name:
            check_name(component.name)
        if os.path.lexists(component):
            require(not is_link(component), "Symlink or reparse-point traversal is prohibited")
    if exists:
        require(path.is_dir(), "Root or temporary directory does not exist")
    return path


def key_path(path):
    return str(Path(path)).replace("\\", "/").casefold()


def inside(path, directory):
    a, b = key_path(path), key_path(directory).rstrip("/")
    return a == b or a.startswith(b + "/")


def target_path(root, relative):
    root = absolute_path(root, exists=True)
    path = root.joinpath(*relative_path(relative).split("/"))
    absolute_path(path)
    require(inside(path, root), "File escapes its declared root")
    if os.path.lexists(path):
        require(path.is_file(), "Only explicitly listed regular files are supported")
        require(stat.S_ISREG(path.stat().st_mode), "Special files are prohibited")
    return path


def state(path):
    absolute_path(path)
    if not os.path.lexists(path):
        return {"exists": False}
    require(Path(path).is_file(), "Expected a regular file")
    before = Path(path).stat()
    digest = sha_file(path)
    after = Path(path).stat()
    require((before.st_size, before.st_mtime_ns, before.st_ino) ==
            (after.st_size, after.st_mtime_ns, after.st_ino), "File changed while reading")
    return {"exists": True, "sha256": digest, "size": after.st_size,
            "mode": stat.S_IMODE(after.st_mode)}


def same_state(actual, expected):
    if actual.get("exists") != expected.get("exists"):
        return False
    return not actual.get("exists") or (
        actual.get("sha256") == expected.get("sha256") and
        actual.get("size") == expected.get("size"))


def config(data):
    require(isinstance(data, dict) and isinstance(data.get("roots"), list)
            and data["roots"], "Configuration requires a nonempty roots list")
    roots, files, targets = {}, [], set()
    for item in data["roots"]:
        require(isinstance(item, dict), "Invalid root record")
        ident = item.get("id", "")
        require(isinstance(ident, str) and re.fullmatch(r"[A-Za-z0-9_-]+", ident)
                and ident.casefold() not in {x.casefold() for x in roots}, "Invalid or duplicate root ID")
        root = absolute_path(item.get("root", ""), exists=True)
        require(isinstance(item.get("paths"), list), "Root paths must be an explicit file list")
        roots[ident] = str(root)
        for raw in item["paths"]:
            rel = relative_path(raw)
            path = target_path(root, rel)
            require(key_path(path) not in targets, "Duplicate file across declared roots")
            targets.add(key_path(path))
            files.append({"root_id": ident, "path": rel})
    require(files or data.get("delete"), "No files were explicitly selected")
    return roots, files


def load_json(path):
    absolute_path(path)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def temp_root(value):
    return absolute_path(value, exists=True)


def same_volume(path, temporary):
    ancestor = Path(path)
    while not ancestor.exists():
        ancestor = ancestor.parent
    require(ancestor.stat().st_dev == temporary.stat().st_dev,
            "Temporary and destination paths must be on the same volume")


def stage(temporary, destination):
    absolute_path(temporary, exists=True)
    absolute_path(destination)
    same_volume(destination, temporary)
    fd, name = tempfile.mkstemp(prefix="skill-release-", suffix=".tmp", dir=temporary)
    return fd, Path(name)


def ensure_directory(path):
    absolute_path(path)
    Path(path).mkdir(parents=True, exist_ok=True)
    absolute_path(path, exists=True)


def atomic_bytes(path, raw, temporary):
    fd, pending = stage(temporary, path)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        absolute_path(path)
        os.replace(pending, path)
    finally:
        if pending.exists():
            pending.unlink()


def save_record(path, payload, temporary):
    raw = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic_bytes(path, raw, temporary)
    atomic_bytes(Path(path).with_suffix(".sha256"),
                 (hashlib.sha256(raw).hexdigest() + "\n").encode("ascii"), temporary)


def checked_record(path):
    path = absolute_path(path)
    checksum = absolute_path(path.with_suffix(".sha256"))
    require(path.is_file() and checksum.is_file(), "Record and SHA sidecar are required")
    expected = checksum.read_text(encoding="ascii").strip()
    require(re.fullmatch(r"[0-9a-f]{64}", expected) and sha_file(path) == expected,
            "Record SHA mismatch")
    return load_json(path)


def prepare_output(output, roots, files, temporary, *, create):
    output = absolute_path(output)
    same_volume(output, temporary)
    for item in files:
        require(not inside(target_path(roots[item["root_id"]], item["path"]), output),
                "Output directory overlaps explicitly managed files")
    if output.exists():
        require(output.is_dir() and not any(output.iterdir()), "Output directory must be empty")
    if create:
        ensure_directory(output)
    return output


def snapshot(data, output, temporary):
    roots, files = config(data)
    temporary = temp_root(temporary)
    output = prepare_output(output, roots, files, temporary, create=True)
    fd, pending = stage(temporary, output / "snapshot.zip")
    os.close(fd)
    records = []
    try:
        with zipfile.ZipFile(pending, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for item in files:
                source = target_path(roots[item["root_id"]], item["path"])
                before = state(source)
                record = {**item, **before}
                if before["exists"]:
                    member = "files/" + item["root_id"] + "/" + item["path"]
                    record["member"] = member
                    digest = hashlib.sha256()
                    with source.open("rb") as src, archive.open(member, "w", force_zip64=True) as dst:
                        for chunk in iter(lambda: src.read(1024 * 1024), b""):
                            digest.update(chunk)
                            dst.write(chunk)
                    require(digest.hexdigest() == before["sha256"] and
                            same_state(state(source), before), "Source changed during snapshot")
                records.append(record)
        for record in records:
            require(same_state(state(target_path(roots[record["root_id"]], record["path"])), record),
                    "Source changed before snapshot completion")
        payload = {"schema": SNAPSHOT_SCHEMA, "created_at": stamp(), "roots": roots,
                   "archive": "snapshot.zip", "archive_sha256": sha_file(pending), "files": records}
        os.replace(pending, output / "snapshot.zip")
        save_record(output / "manifest.json", payload, temporary)
        verify(output / "manifest.json")
        return {"status": "snapshotted", "manifest": str(output / "manifest.json"),
                "files": len(records), "archive_sha256": payload["archive_sha256"]}
    finally:
        if pending.exists():
            pending.unlink()


def validate_snapshot(payload):
    require(payload.get("schema") == SNAPSHOT_SCHEMA and payload.get("archive") == "snapshot.zip",
            "Unsupported snapshot format")
    roots = payload.get("roots")
    require(isinstance(roots, dict) and roots and isinstance(payload.get("files"), list),
            "Invalid snapshot roots or files")
    for ident, root in roots.items():
        require(re.fullmatch(r"[A-Za-z0-9_-]+", ident) and isinstance(root, str) and
                (Path(root).is_absolute() or PureWindowsPath(root).is_absolute()), "Invalid snapshot root")
    seen, members = set(), {}
    for item in payload["files"]:
        require(isinstance(item, dict) and item.get("root_id") in roots, "Unknown snapshot root")
        rel = relative_path(item.get("path"))
        require(rel == item["path"], "Snapshot path is not canonical")
        key = (item["root_id"].casefold(), rel.casefold())
        require(key not in seen, "Duplicate snapshot path")
        seen.add(key)
        require(isinstance(item.get("exists"), bool), "Invalid snapshot existence state")
        if item["exists"]:
            member = "files/" + item["root_id"] + "/" + rel
            require(item.get("member") == member and
                    re.fullmatch(r"[0-9a-f]{64}", str(item.get("sha256", ""))) and
                    isinstance(item.get("size"), int) and item["size"] >= 0,
                    "Invalid snapshot file record")
            members[member] = item
        else:
            require(not any(k in item for k in ("member", "sha256", "size")), "Invalid absent-file record")
    return members


def verify(manifest):
    manifest = absolute_path(manifest)
    payload = checked_record(manifest)
    members = validate_snapshot(payload)
    archive_path = absolute_path(manifest.parent / "snapshot.zip")
    require(archive_path.is_file() and sha_file(archive_path) == payload.get("archive_sha256"),
            "Archive SHA mismatch")
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(n.casefold() for n in names)) and set(names) == set(members),
                "Unexpected, duplicate, or missing ZIP entries")
        for info in archive.infolist():
            relative_path(info.filename)
            require(not info.is_dir() and not (info.flag_bits & 1), "Directory or encrypted ZIP entry")
            mode = info.external_attr >> 16
            require(stat.S_IFMT(mode) in (0, stat.S_IFREG), "Nonregular ZIP entry")
            item = members[info.filename]
            require(info.file_size == item["size"], "ZIP size mismatch")
            digest = hashlib.sha256()
            with archive.open(info) as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            require(digest.hexdigest() == item["sha256"], "Archived file SHA mismatch")
    return payload


def native_targets(payload):
    data = {"roots": [{"id": ident, "root": root,
                        "paths": [x["path"] for x in payload["files"] if x["root_id"] == ident]}
                       for ident, root in payload["roots"].items()]}
    roots, _ = config(data)
    return roots, {(x["root_id"], x["path"]): x for x in payload["files"]}


def check_expected(roots, items, field=None):
    for item in items:
        wanted = item[field] if field else item
        actual = state(target_path(roots[item["root_id"]], item["path"]))
        require(same_state(actual, wanted), "Target drift: " + item["root_id"] + "/" + item["path"])


def file_state_only(item):
    return {k: item[k] for k in ("exists", "sha256", "size", "mode") if k in item}


def require_runtime_file(relative):
    require(Path(relative).name.casefold() not in {
        "project_state.json", "current_state.md", "current_state.generated.md", "全局工作台.md"},
        "Project state is snapshot-only here; apply or rollback it through the state CAS API")


def commit_plan(roots, plan, readers, output, temporary, baseline, operation):
    record = {"schema": DEPLOYMENT_SCHEMA, "operation": operation, "created_at": stamp(),
              "baseline_manifest_sha256": sha_file(baseline), "roots": roots,
              "status": "applying", "files": [
                  {"root_id": x["root_id"], "path": x["path"], "before": x["before"],
                   "after": x["before"]} for x in plan]}
    staged = []
    try:
        for item in plan:
            target = target_path(roots[item["root_id"]], item["path"])
            if item["after"]["exists"]:
                fd, pending = stage(temporary, target)
                staged.append(pending)
                with os.fdopen(fd, "wb") as dst, readers[(item["root_id"], item["path"])]() as src:
                    for chunk in iter(lambda: src.read(1024 * 1024), b""):
                        dst.write(chunk)
                    dst.flush()
                    os.fsync(dst.fileno())
                require(same_state(state(pending), item["after"]), "Candidate or archive changed while staging")
                os.chmod(pending, item["after"].get("mode", 0o644))
            else:
                staged.append(None)
        check_expected(roots, plan, "before")
        save_record(output / "deployment.json", record, temporary)
        for index, item in enumerate(plan):
            target = target_path(roots[item["root_id"]], item["path"])
            check_expected(roots, [item], "before")
            if item["after"]["exists"]:
                ensure_directory(target.parent)
                target_path(roots[item["root_id"]], item["path"])
                os.replace(staged[index], target)
            elif item["before"]["exists"]:
                target.unlink()  # One explicit, hash-checked file; never a directory.
            record["files"][index]["after"] = item["after"]
            save_record(output / "deployment.json", record, temporary)
        check_expected(roots, plan, "after")
        record["status"] = "applied"
        save_record(output / "deployment.json", record, temporary)
    except Exception:
        if (output / "deployment.json").exists():
            record["status"] = "apply_failed"
            save_record(output / "deployment.json", record, temporary)
        raise
    finally:
        for pending in staged:
            if pending is not None and pending.exists():
                pending.unlink()
    return {"status": "applied", "operation": operation, "files": len(plan),
            "deployment": str(output / "deployment.json")}


def apply_candidate(manifest, candidate_data, output, temporary, *, apply=False):
    manifest = absolute_path(manifest)
    payload = verify(manifest)
    roots, baseline = native_targets(payload)
    source_roots, candidates = config(candidate_data)
    require(set(source_roots) <= set(roots), "Candidate root IDs must exist in baseline")
    plan, readers, seen = [], {}, set()
    for item in candidates:
        key = item["root_id"], item["path"]
        require_runtime_file(key[1])
        target = target_path(roots[key[0]], key[1])
        before = file_state_only(baseline.get(key, {"exists": False}))
        if key in baseline:
            check_expected(roots, [{**item, "before": before}], "before")
        else:
            require(not state(target)["exists"], "New target already exists")
        source = target_path(source_roots[key[0]], key[1])
        after = state(source)
        require(after["exists"], "Candidate file is missing; use an explicit delete record")
        require(key_path(source) != key_path(target), "Candidate and destination must be separate files")
        plan.append({**item, "before": before, "after": after})
        readers[key] = lambda path=source: path.open("rb")
        seen.add(key)
    for item in candidate_data.get("delete", []):
        require(isinstance(item, dict) and item.get("root_id") in roots, "Invalid deletion root")
        key = item["root_id"], relative_path(item.get("path"))
        require_runtime_file(key[1])
        require(key in baseline and baseline[key]["exists"] and key not in seen,
                "Deletion must name one existing baseline file exactly once")
        plan.append({"root_id": key[0], "path": key[1], "before": file_state_only(baseline[key]),
                     "after": {"exists": False}})
        seen.add(key)
    # Nested roots are allowed, duplicate physical targets are not.
    targets = [key_path(target_path(roots[x["root_id"]], x["path"])) for x in plan]
    require(len(targets) == len(set(targets)), "Candidate scope aliases a target across roots")
    require(plan, "Empty candidate plan")
    check_expected(roots, plan, "before")
    temporary = temp_root(temporary)
    out = prepare_output(output, roots, [*payload["files"], *plan], temporary, create=False)
    for item in candidates:
        require(not inside(target_path(source_roots[item["root_id"]], item["path"]), out),
                "Output directory overlaps candidate files")
    if not apply:
        return {"status": "dry_run", "operation": "apply", "files": plan}
    ensure_directory(out)
    return commit_plan(roots, plan, readers, out, temporary, manifest, "apply")


def declared_keys(items, roots, label):
    require(isinstance(items, list), label + " must be a list")
    result = set()
    for item in items:
        require(isinstance(item, dict) and item.get("root_id") in roots,
                "Invalid root in " + label)
        key = item["root_id"], relative_path(item.get("path"))
        require(key not in result, "Duplicate entry in " + label)
        result.add(key)
    return result


def capture(manifest, observed_data, output, temporary, *, apply=False):
    """Record caller-selected existing edits without claiming to have applied them."""
    manifest = absolute_path(manifest)
    payload = verify(manifest)
    roots, baseline = native_targets(payload)
    selected_roots, selected = config(observed_data)
    require(not observed_data.get("delete"), "Capture uses explicit paths, not candidate delete directives")
    require(set(selected_roots) <= set(roots) and all(
        key_path(root) == key_path(roots[ident]) for ident, root in selected_roots.items()),
        "Observed root IDs and paths must match baseline targets")
    new_files = declared_keys(observed_data.get("new_files", []), roots, "new_files")
    scope = {(x["root_id"], x["path"]) for x in selected}
    require(new_files <= scope and not (new_files & set(baseline)),
            "new_files must name selected files absent from the baseline list")
    baseline_targets = {key_path(target_path(roots[k[0]], k[1])): k for k in baseline}
    changes, observations = [], []
    for item in selected:
        key = item["root_id"], item["path"]
        require_runtime_file(key[1])
        target = target_path(roots[key[0]], key[1])
        require(key in baseline or (key in new_files and key_path(target) not in baseline_targets),
                "Unlisted files require an explicit new_files declaration without root aliases")
        before = file_state_only(baseline.get(key, {"exists": False}))
        after = state(target)
        require(key not in new_files or after["exists"], "Declared new file does not exist")
        observations.append({**item, "after": after})
        if not same_state(before, after):
            changes.append({**item, "before": before, "after": after,
                            "before_source": "baseline" if key in baseline else "operator_declared_new_file"})
    temporary = temp_root(temporary)
    out = prepare_output(output, roots, [*payload["files"], *selected], temporary, create=False)
    check_expected(roots, observations, "after")
    if not apply:
        return {"status": "dry_run", "operation": "observed_edits", "files": changes,
                "unchanged_files": len(selected) - len(changes), "managed_files_modified": False}
    if not changes:
        return {"status": "no_changes", "operation": "observed_edits", "files": 0,
                "managed_files_modified": False}
    record = {"schema": DEPLOYMENT_SCHEMA, "operation": "observed_edits", "created_at": stamp(),
              "baseline_manifest_sha256": sha_file(manifest), "roots": roots, "status": "captured",
              "observed_scope": selected,
              "operator_declared_new_files": [{"root_id": k[0], "path": k[1]} for k in sorted(new_files)],
              "files": changes, "managed_files_modified": False,
              "provenance": "Observed current bytes only; this tool did not perform or approve these edits."}
    ensure_directory(out)
    save_record(out / "deployment.json", record, temporary)
    try:
        check_expected(roots, observations, "after")
    except Exception:
        record["status"] = "capture_failed"
        save_record(out / "deployment.json", record, temporary)
        raise
    return {"status": "captured", "operation": "observed_edits", "files": len(changes),
            "unchanged_files": len(selected) - len(changes), "managed_files_modified": False,
            "deployment": str(out / "deployment.json")}


def restore(manifest, deployment, output, temporary, *, apply=False):
    manifest = absolute_path(manifest)
    payload = verify(manifest)
    roots, baseline = native_targets(payload)
    deployed = checked_record(absolute_path(deployment))
    require(deployed.get("schema") == DEPLOYMENT_SCHEMA and
            deployed.get("status") in {"applied", "apply_failed", "captured"} and
            deployed.get("baseline_manifest_sha256") == sha_file(manifest) and
            deployed.get("roots") == roots, "Deployment is not bound to this baseline")
    require(isinstance(deployed.get("files"), list) and deployed["files"], "Empty deployment record")
    captured = deployed["status"] == "captured"
    if captured:
        require(deployed.get("operation") == "observed_edits" and
                deployed.get("managed_files_modified") is False, "Invalid captured-edit provenance")
        observed_scope = declared_keys(deployed.get("observed_scope"), roots, "observed_scope")
        declared_new = declared_keys(deployed.get("operator_declared_new_files"), roots, "operator_declared_new_files")
        require(declared_new <= observed_scope and not (declared_new & set(baseline)),
                "Invalid captured new-file declaration")
    else:
        require(deployed.get("operation") in {"apply", "restore"}, "Invalid deployment operation")
    baseline_targets = {key_path(target_path(roots[k[0]], k[1])): k for k in baseline}
    plan, seen = [], set()
    for item in deployed["files"]:
        require(isinstance(item, dict) and item.get("root_id") in roots, "Invalid deployment root")
        key = item["root_id"], relative_path(item.get("path"))
        require_runtime_file(key[1])
        target = key_path(target_path(roots[key[0]], key[1]))
        require(target not in seen, "Duplicate deployed target")
        seen.add(target)
        require(key in baseline or target not in baseline_targets, "Deployed file aliases a baseline path")
        if captured:
            require(key in observed_scope and (key in baseline or key in declared_new),
                    "Captured file is outside the declared scope")
            require(item.get("before_source") == (
                "baseline" if key in baseline else "operator_declared_new_file"),
                "Invalid captured baseline provenance")
        original = file_state_only(baseline.get(key, {"exists": False}))
        require(item.get("before") == original, "Deployment invented a baseline file state")
        require(isinstance(item.get("after"), dict) and isinstance(item["after"].get("exists"), bool),
                "Invalid deployed file state")
        plan.append({"root_id": key[0], "path": key[1], "before": item["after"], "after": original})
    check_expected(roots, plan, "before")
    temporary = temp_root(temporary)
    out = prepare_output(output, roots, [*payload["files"], *plan], temporary, create=False)
    if not apply:
        return {"status": "dry_run", "operation": "restore", "files": plan}
    current_config = {"roots": [{"id": ident, "root": root,
                                  "paths": [x["path"] for x in plan if x["root_id"] == ident]}
                                 for ident, root in roots.items()]}
    snapshot(current_config, out, temporary)
    with zipfile.ZipFile(manifest.parent / "snapshot.zip") as archive:
        readers = {(x["root_id"], x["path"]):
                   (lambda member=baseline[(x["root_id"], x["path"])]["member"]: archive.open(member))
                   for x in plan if x["after"]["exists"]}
        result = commit_plan(roots, plan, readers, out, temporary, out / "manifest.json", "restore")
    result["pre_restore_manifest"] = str(out / "manifest.json")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    snap = commands.add_parser("snapshot")
    snap.add_argument("--config", required=True, type=Path)
    check = commands.add_parser("verify")
    check.add_argument("--manifest", required=True, type=Path)
    candidate = commands.add_parser("apply")
    candidate.add_argument("--candidate-config", required=True, type=Path)
    back = commands.add_parser("restore")
    back.add_argument("--deployment", required=True, type=Path)
    observed = commands.add_parser("capture")
    observed.add_argument("--config", required=True, type=Path)
    for sub in (candidate, back, observed):
        sub.add_argument("--manifest", required=True, type=Path)
        sub.add_argument("--apply", action="store_true", help="Execute; omitted means dry-run")
    for sub in (snap, candidate, back, observed):
        sub.add_argument("--output-dir", required=True, type=Path)
        sub.add_argument("--temp-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "snapshot":
            result = snapshot(load_json(absolute_path(args.config)), args.output_dir, args.temp_dir)
        elif args.command == "verify":
            payload = verify(args.manifest)
            result = {"status": "verified", "files": len(payload["files"]),
                      "archive_sha256": payload["archive_sha256"]}
        elif args.command == "apply":
            result = apply_candidate(args.manifest, load_json(absolute_path(args.candidate_config)),
                                     args.output_dir, args.temp_dir, apply=args.apply)
        elif args.command == "capture":
            result = capture(args.manifest, load_json(absolute_path(args.config)),
                             args.output_dir, args.temp_dir, apply=args.apply)
        else:
            result = restore(args.manifest, args.deployment, args.output_dir, args.temp_dir, apply=args.apply)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ReleaseError, OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile, RuntimeError) as exc:
        print(json.dumps({"status": "refused", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
