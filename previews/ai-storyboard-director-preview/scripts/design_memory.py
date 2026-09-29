#!/usr/bin/env python3
"""Save directing decisions and gate deterministic constraints, not artistic quality."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import tempfile

STATE = ".director_design/state.json"
LOCK = ".director_design/write.lock"
TOPICS = {
    "framing": ["framing-and-axis.md", "cinematography-design-engine.md"],
    "continuity": ["framing-and-axis.md", "production-contract.md"],
    "motion": ["cinematography-design-engine.md", "shot-design-engine.md"],
    "optics": ["cinematography-design-engine.md"],
    "blocking": ["shot-design-engine.md", "framing-and-axis.md"],
    "delivery": ["production-contract.md"],
}
ROOT_FIELDS = {"schema_version", "project_id", "revision", "source", "film_intent",
               "locked_facts", "candidate_decisions", "scenes", "history"}


class GateError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def require(condition, code, message):
    if not condition:
        raise GateError(code, message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def scene_digest(scene):
    return digest(canonical(scene))


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "DUPLICATE_KEY", f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def finite_values(value):
    if isinstance(value, float):
        require(math.isfinite(value), "NONFINITE_NUMBER", "NaN and infinity are forbidden")
    elif isinstance(value, dict):
        for item in value.values():
            finite_values(item)
    elif isinstance(value, list):
        for item in value:
            finite_values(item)


def parse_json(data):
    def reject_constant(value):
        raise GateError("NONFINITE_NUMBER", f"Forbidden JSON number: {value}")
    try:
        value = json.loads(data.decode("utf-8-sig"), object_pairs_hook=unique_object,
                           parse_constant=reject_constant)
    except (ValueError, UnicodeError) as exc:
        raise GateError("INVALID_JSON", str(exc)) from exc
    finite_values(value)
    return value


def project_root(value):
    root = Path(value).resolve(strict=True)
    require(root.is_dir(), "INVALID_ROOT", "Project root must be an existing directory")
    return root


def inside(root, value):
    require(isinstance(value, str) and value.strip(), "INVALID_PATH", "A path is required")
    path = Path(value)
    require(not path.drive or path.is_absolute(), "PATH_ESCAPE", "Drive-relative paths are forbidden")
    require(".." not in path.parts, "PATH_ESCAPE", "Parent traversal is forbidden")
    # A drive colon is valid only in the anchor; all other colons are Windows streams.
    parts = path.parts[1:] if path.anchor else path.parts
    require(not any(":" in part for part in parts), "PATH_ESCAPE", "Alternate streams are forbidden")
    resolved = (path if path.is_absolute() else root / path).resolve()
    require(resolved.is_relative_to(root) and resolved != root,
            "PATH_ESCAPE", "Path must remain inside the project root")
    return resolved


def text_field(value, name):
    require(isinstance(value, str) and bool(value.strip()), "MISSING_INFORMATION", f"{name} needs nonempty text")


def object_field(value, name):
    require(isinstance(value, dict), "INVALID_FORMAT", f"{name} must be an object")


def number(value, name):
    require(type(value) in (int, float) and math.isfinite(value),
            "INVALID_NUMBER", f"{name} must be a finite number")


def required_keys(value, keys, name):
    object_field(value, name)
    missing = set(keys) - set(value)
    require(not missing, "MISSING_INFORMATION", f"{name} missing: {', '.join(sorted(missing))}")


def identify(items, name, fields):
    require(isinstance(items, list), "INVALID_FORMAT", f"{name} must be a list")
    found = set()
    for item in items:
        required_keys(item, ["id", *fields], name)
        text_field(item["id"], f"{name}.id")
        require(item["id"] not in found, "DUPLICATE_ID", f"Duplicate {name} id: {item['id']}")
        found.add(item["id"])
        for field in fields:
            text_field(item[field], f"{name}.{field}")


def read_source(root, source):
    path = inside(root, source)
    require(path.is_file(), "SOURCE_MISSING", "Script source must be an existing file")
    data = path.read_bytes()
    try:
        lines = data.decode("utf-8-sig").splitlines()
    except UnicodeError as exc:
        raise GateError("SOURCE_ENCODING", "Source must be UTF-8 plain text") from exc
    require(bool(lines), "SOURCE_EMPTY", "Script source cannot be empty")
    return {"path": path.relative_to(root).as_posix(), "sha256": digest(data),
            "line_count": len(lines)}, lines


def verify_source(root, state):
    actual, lines = read_source(root, state["source"]["path"])
    require(actual == state["source"], "SOURCE_DRIFT", "Script changed; explicit amendment and redesign are required")
    return lines


def point(value, name):
    require(isinstance(value, list) and len(value) == 2, "INVALID_GEOMETRY", f"{name} must be [world_x, world_z]")
    for coordinate in value:
        number(coordinate, name)


def inspect_axis(axis, shots, scene_id):
    required_keys(axis, ["status"], f"{scene_id}.axis")
    status = axis["status"]
    if status in ("not_applicable", "needs_geometry_review"):
        text_field(axis.get("reason"), f"{scene_id}.axis.reason")
        return [scene_id] if status == "needs_geometry_review" else []
    require(status == "defined", "INVALID_GEOMETRY", "Axis status must be defined, not_applicable, or needs_geometry_review")
    required_keys(axis, ["start", "end", "allowed_side"], f"{scene_id}.axis")
    point(axis["start"], "axis.start")
    point(axis["end"], "axis.end")
    x0, z0 = axis["start"]
    dx, dz = axis["end"][0] - x0, axis["end"][1] - z0
    length = math.hypot(dx, dz)
    require(math.isfinite(length) and length > 1e-9, "INVALID_GEOMETRY", "Axis endpoints must differ and remain finite")
    require(axis["allowed_side"] in ("positive", "negative"), "INVALID_GEOMETRY", "allowed_side must be positive or negative")
    multiplier = 1 if axis["allowed_side"] == "positive" else -1
    for shot in shots:
        path = shot["camera"].get("path")
        require(isinstance(path, list) and len(path) > 0, "MISSING_GEOMETRY", f"{shot['shot_id']} needs the full piecewise-linear camera path")
        for position in path:
            point(position, "camera.path point")
            signed_distance = (dx * (position[1] - z0) - dz * (position[0] - x0)) / length
            require(math.isfinite(signed_distance) and multiplier * signed_distance > 1e-9,
                    "AXIS_CROSSING", f"{shot['shot_id']} is on or beyond the permitted axis side; explicit axis redesign or geometry review is required")
    return []


def state_changes(shot):
    before, after = shot["enter_state"], shot["exit_state"]
    require(set(before) == set(after), "STATE_KEYS_CHANGED", "Track the same keys within a shot; use null for absence")
    changed = {key for key in before if before[key] != after[key]}
    entries = shot.get("state_changes", [])
    require(isinstance(entries, list), "INVALID_FORMAT", "state_changes must be a list")
    declared = set()
    for entry in entries:
        required_keys(entry, ["key", "from", "to", "action"], "state_changes")
        key = entry["key"]
        text_field(key, "state_changes.key")
        require(key not in declared, "DUPLICATE_ID", f"Duplicate state change: {key}")
        require(key in changed and entry["from"] == before[key] and entry["to"] == after[key],
                "STATE_CHANGE_MISMATCH", f"Declared change does not match states: {key}")
        text_field(entry["action"], "state_changes.action")
        declared.add(key)
    require(declared == changed, "UNEXPLAINED_STATE_CHANGE", f"Visible action record missing for: {sorted(changed - declared)}")


def validate_state(state, allow_empty=False):
    required_keys(state, ROOT_FIELDS, "state")
    require(set(state) == ROOT_FIELDS, "UNKNOWN_FIELD", "Unexpected top-level state field")
    require(type(state["schema_version"]) is int and state["schema_version"] == 1, "SCHEMA_VERSION", "schema_version must be 1")
    text_field(state["project_id"], "project_id")
    require(type(state["revision"]) is int and state["revision"] >= 0, "INVALID_FORMAT", "revision must be a nonnegative integer")
    source = state["source"]
    required_keys(source, ["path", "sha256", "line_count"], "source")
    text_field(source["path"], "source.path")
    require(isinstance(source["sha256"], str) and len(source["sha256"]) == 64 and
            all(char in "0123456789abcdef" for char in source["sha256"]), "INVALID_FORMAT", "source.sha256 must be lowercase SHA-256")
    require(type(source["line_count"]) is int and source["line_count"] > 0, "INVALID_FORMAT", "source.line_count must be a positive integer")
    required_keys(state["film_intent"], ["intent", "rationale"], "film_intent")
    identify(state["locked_facts"], "locked_facts", ["statement"])
    identify(state["candidate_decisions"], "candidate_decisions", ["decision", "rationale"])
    require(isinstance(state["history"], list), "INVALID_FORMAT", "history must be a list")
    require(isinstance(state["scenes"], list), "INVALID_FORMAT", "scenes must be a list")
    if allow_empty and not state["scenes"]:
        return []
    text_field(state["film_intent"]["intent"], "film_intent.intent")
    text_field(state["film_intent"]["rationale"], "film_intent.rationale")
    require(bool(state["scenes"]), "MISSING_INFORMATION", "No valid scenes exist; redesign is required")
    seen_scenes, seen_shots, reviews, previous = set(), set(), [], None
    for scene in state["scenes"]:
        required_keys(scene, ["scene_id", "source_lines", "dramatic_change", "director_intent",
                             "enter_state", "exit_state", "previous_scene", "duration_seconds",
                             "design_questions", "knowledge_topics", "axis", "shots"], "scene")
        sid = scene["scene_id"]
        text_field(sid, "scene_id")
        require(sid not in seen_scenes, "DUPLICATE_ID", f"Duplicate scene id: {sid}")
        seen_scenes.add(sid)
        for key in ("dramatic_change", "director_intent"):
            text_field(scene[key], f"{sid}.{key}")
        for key in ("enter_state", "exit_state"):
            object_field(scene[key], f"{sid}.{key}")
        line_range = scene["source_lines"]
        require(isinstance(line_range, list) and len(line_range) == 2 and
                all(type(item) is int for item in line_range) and
                1 <= line_range[0] <= line_range[1] <= source["line_count"],
                "SOURCE_RANGE", f"Invalid source line range in {sid}")
        for key in ("design_questions", "knowledge_topics"):
            require(isinstance(scene[key], list) and bool(scene[key]), "MISSING_INFORMATION", f"{sid}.{key} needs a nonempty list")
            for item in scene[key]:
                text_field(item, f"{sid}.{key}")
        require(all(topic in TOPICS for topic in scene["knowledge_topics"]), "UNKNOWN_TOPIC", f"Allowed topics: {', '.join(TOPICS)}")
        if previous is None:
            require(scene["previous_scene"] is None, "PREVIOUS_SCENE", "First scene must have previous_scene:null")
        else:
            require(scene["previous_scene"] == {"scene_id": previous["scene_id"], "sha256": scene_digest(previous)},
                    "STALE_UPSTREAM", f"{sid} must bind the preceding scene's current hash")
            require(scene["enter_state"] == previous["exit_state"] or bool(scene.get("entry_changes")),
                    "CONTINUITY_BREAK", f"{sid} entrance differs from prior scene exit without a recorded transition")
            state_changes({"enter_state": previous["exit_state"], "exit_state": scene["enter_state"],
                           "state_changes": scene.get("entry_changes", [])})
        number(scene["duration_seconds"], "duration_seconds")
        require(scene["duration_seconds"] > 0, "INVALID_TIME", "Scene duration must be positive")
        shots = scene["shots"]
        require(isinstance(shots, list) and bool(shots), "MISSING_INFORMATION", f"{sid} needs shots")
        end, current = 0, scene["enter_state"]
        for shot in shots:
            required_keys(shot, ["shot_id", "start", "end", "viewing_task", "framing", "camera",
                                "motion", "ending", "enter_state", "exit_state"], "shot")
            shot_id = shot["shot_id"]
            text_field(shot_id, "shot_id")
            require(shot_id not in seen_shots, "DUPLICATE_ID", f"Duplicate shot id: {shot_id}")
            seen_shots.add(shot_id)
            for key in ("viewing_task", "framing", "ending"):
                text_field(shot[key], f"{shot_id}.{key}")
            for key in ("camera", "motion"):
                object_field(shot[key], f"{shot_id}.{key}")
                require(bool(shot[key]), "MISSING_INFORMATION", f"{shot_id}.{key} cannot be empty")
            for key in ("enter_state", "exit_state"):
                object_field(shot[key], f"{shot_id}.{key}")
            number(shot["start"], "shot.start")
            number(shot["end"], "shot.end")
            require(0 <= shot["start"] < shot["end"] <= scene["duration_seconds"], "INVALID_TIME", f"Invalid shot interval: {shot_id}")
            require(abs(shot["start"] - end) <= 1e-7, "TIME_GAP_OR_OVERLAP", f"Shot gap or overlap before {shot_id}")
            require(shot["enter_state"] == current, "CONTINUITY_BREAK", f"{shot_id} entrance differs from preceding state")
            state_changes(shot)
            end, current = shot["end"], shot["exit_state"]
        require(abs(end - scene["duration_seconds"]) <= 1e-7, "TIME_GAP_OR_OVERLAP", f"Shots do not fill {sid}")
        require(current == scene["exit_state"], "CONTINUITY_BREAK", f"{sid} exit differs from final shot")
        reviews.extend(inspect_axis(scene["axis"], shots, sid))
        previous = scene
    return reviews


def load_state(root, source_check=True):
    path = inside(root, STATE)
    require(path.is_file(), "STATE_MISSING", "Initialize project design memory first")
    raw = path.read_bytes()
    state = parse_json(raw)
    validate_state(state, allow_empty=True)
    if source_check:
        verify_source(root, state)
    return state, digest(raw)


def cas(state, sha256, args):
    require(state["revision"] == args.expected_revision and sha256 == args.expected_sha256.lower(),
            "STALE_REVISION", "Revision/hash changed; read current context and merge before retrying")


@contextmanager
def write_lock(root):
    directory = inside(root, ".director_design")
    directory.mkdir(exist_ok=True)
    lock = inside(root, LOCK)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise GateError("LOCK_EXISTS", "A write lock exists; this command will not remove it") from exc
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            stream.write(str(os.getpid()))
        yield
    finally:
        lock.unlink()


def atomic_write(root, relative, data, new=False):
    target = inside(root, relative)
    require(target.parent.is_dir(), "OUTPUT_PARENT_MISSING", "Output parent directory must already exist")
    require(not new or not target.exists(), "OUTPUT_EXISTS", "Refusing to overwrite existing output")
    fd, name = tempfile.mkstemp(prefix=".design-write-", dir=target.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        require(inside(root, relative) == target, "PATH_CHANGED", "Output path changed during write")
        if new:
            os.link(temporary, target)  # Atomic new name; never replaces existing files.
        else:
            os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def save_state(root, state, new=False):
    data = json.dumps(state, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8") + b"\n"
    atomic_write(root, STATE, data, new=new)
    return digest(data)


def result(memory, sha256, **extra):
    return {"ok": True, "project_id": memory["project_id"], "revision": memory["revision"],
            "state_sha256": sha256, "machine_constraints_only": True,
            "text_semantics_verified": False, **extra}


def selected(state, scene_id):
    for scene in state["scenes"]:
        if scene["scene_id"] == scene_id:
            return scene
    raise GateError("SCENE_MISSING", f"No current scene: {scene_id}")


def knowledge(topics):
    references = Path(__file__).resolve().parent.parent / "references"
    names = list(dict.fromkeys(name for topic in ["framing", "continuity", *topics] for name in TOPICS[topic]))
    items = []
    for name in names:
        path = references / name
        require(path.is_file(), "KNOWLEDGE_MISSING", f"Bundled reference missing: {name}")
        items.append({"path": str(path), "sha256": digest(path.read_bytes()), "must_read": True})
    return items


def initialize(args, root):
    source, _ = read_source(root, args.source)
    text_field(args.project_id, "project_id")
    state = {"schema_version": 1, "project_id": args.project_id, "revision": 0,
             "source": source, "film_intent": {"intent": "", "rationale": ""},
             "locked_facts": [], "candidate_decisions": [], "scenes": [], "history": []}
    with write_lock(root):
        require(not inside(root, STATE).exists(), "STATE_EXISTS", "Initialization never replaces existing state")
        sha256 = save_state(root, state, new=True)
    return result(state, sha256, design_ready=False, state=state, state_path=str(inside(root, STATE)))


def context(args, root):
    state, sha256 = load_state(root)
    scene = selected(state, args.scene) if args.scene else None
    lines = verify_source(root, state)
    index = [{"scene_id": item["scene_id"], "sha256": scene_digest(item),
              "source_lines": item["source_lines"]} for item in state["scenes"]]
    excerpt = None
    if scene:
        first, last = scene["source_lines"]
        excerpt = [{"line": n, "text": lines[n - 1]} for n in range(first, last + 1)]
    output = result(state, sha256, state=state, film_intent=state["film_intent"], locked_facts=state["locked_facts"],
                  candidate_decisions=state["candidate_decisions"], source=state["source"],
                  scene_index=index, scene=scene, scene_sha256=scene_digest(scene) if scene else None,
                  source_excerpt=excerpt, knowledge=knowledge(args.topics if args.topics else (scene["knowledge_topics"] if scene else ["delivery"])),
                  design_ready=bool(state["scenes"]) and not any(item["axis"]["status"] == "needs_geometry_review" for item in state["scenes"]),
                  history_count=len(state["history"]))
    if args.compact:
        output.pop("state")
        output["previous_scene"] = scene["previous_scene"] if scene else None
        if scene:
            needed = {scene["scene_id"]}
            if scene["previous_scene"]:
                needed.add(scene["previous_scene"]["scene_id"])
            output["scene_index"] = [item for item in index if item["scene_id"] in needed]
    return output


def commit(args, root):
    with write_lock(root):
        old, sha256 = load_state(root, source_check=not args.amend)
        cas(old, sha256, args)
        proposed = parse_json(inside(root, args.input).read_bytes())
        object_field(proposed, "proposal")
        require(set(proposed) <= ROOT_FIELDS, "UNKNOWN_FIELD", "Unexpected top-level proposal field")
        proposed.setdefault("revision", old["revision"])
        proposed.setdefault("history", old["history"])
        require(proposed["revision"] == old["revision"], "STALE_REVISION", "Proposal revision must equal expected current revision")
        require(proposed["history"] == old["history"], "HISTORY_CHANGED", "History cannot be edited in a proposal")
        require(proposed.get("project_id") == old["project_id"], "PROJECT_CHANGED", "Stable project_id cannot change")
        if args.amend:
            text_field(args.change_reason, "--change-reason")
            require(proposed.get("scenes") == [], "AMEND_REQUIRES_REDESIGN", "Amendment must invalidate all current scenes with scenes:[]")
            snapshot = {key: value for key, value in old.items() if key != "history"}
            proposed["history"] = old["history"] + [{"change_reason": args.change_reason,
                                                   "previous_state_sha256": sha256, "previous_state": snapshot}]
        else:
            require(not args.change_reason, "AMEND_FLAG_REQUIRED", "--change-reason requires --amend")
            require(proposed.get("source") == old["source"], "SOURCE_CHANGED", "Ordinary commit cannot replace the script source")
            locks = proposed.get("locked_facts", [])
            require(isinstance(locks, list), "INVALID_FORMAT", "locked_facts must be a list")
            require(all(item in locks for item in old["locked_facts"]), "LOCKED_FACT_CHANGED", "Locked fact removed/changed; explicit user-authorized amendment is required")
            next_scenes = proposed.get("scenes", [])
            require(isinstance(next_scenes, list), "INVALID_FORMAT", "scenes must be a list")
            next_ids = {item.get("scene_id") for item in next_scenes if isinstance(item, dict)}
            require(all(item["scene_id"] in next_ids for item in old["scenes"]),
                    "SCENE_REMOVED", "A saved scene was omitted; explicit scope amendment is required")
        reviews = validate_state(proposed, allow_empty=args.amend)
        verify_source(root, proposed)
        proposed["revision"] = old["revision"] + 1
        sha256 = save_state(root, proposed)
    return result(proposed, sha256, design_ready=bool(proposed["scenes"]) and not reviews,
                  needs_geometry_review=reviews,
                  scene_index=[{"scene_id": item["scene_id"], "sha256": scene_digest(item)} for item in proposed["scenes"]])


def check(args, root):
    state, sha256 = load_state(root)
    scene = selected(state, args.scene)
    reviews = validate_state(state)
    return result(state, sha256, scene_sha256=scene_digest(scene),
                  status="needs_geometry_review" if reviews else "machine_constraints_passed",
                  ready=not reviews, needs_geometry_review=reviews)


def export(args, root):
    with write_lock(root):
        state, sha256 = load_state(root)
        cas(state, sha256, args)
        scene = selected(state, args.scene)
        reviews = validate_state(state)
        if args.allow_unverified_geometry:
            text_field(args.review_note, "--review-note")
        else:
            require(not args.review_note, "REVIEW_FLAG_REQUIRED", "--review-note requires --allow-unverified-geometry")
            require(not reviews, "NEEDS_GEOMETRY_REVIEW", "Design retained; review geometry or explicitly export an unverified candidate")
        geometry_verified = not reviews and all(item["axis"]["status"] == "defined" for item in state["scenes"])
        text_path = inside(root, args.text)
        payload = text_path.read_bytes()
        try:
            body = payload.decode("utf-8-sig")
        except UnicodeError as exc:
            raise GateError("TEXT_ENCODING", "Delivery text must be UTF-8") from exc
        text_field(body, "delivery text")
        output = inside(root, args.output)
        require(not output.is_relative_to(inside(root, ".director_design")), "RESERVED_OUTPUT", "Exports cannot target internal memory files")
        receipt = result(state, sha256, scene_id=scene["scene_id"], scene_sha256=scene_digest(scene),
                         source=state["source"], text_sha256=digest(payload),
                         text_path=text_path.relative_to(root).as_posix(), text=body,
                         ready=not reviews, geometry_verified=geometry_verified,
                         geometry_scope="recorded_fixed_2d_axis_paths_only", review_note=args.review_note,
                         needs_geometry_review=reviews,
                         delivery_status="unverified_candidate" if reviews else "machine_checked_awaiting_semantic_and_visual_review")
        atomic_write(root, args.output, json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8") + b"\n", new=True)
    return {**receipt, "output_path": str(output)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("init", "context", "commit", "check", "export"):
        sub = commands.add_parser(name)
        sub.add_argument("--project-root", required=True)
        if name == "init":
            sub.add_argument("--project-id", required=True)
            sub.add_argument("--source", required=True)
        if name in ("context", "check", "export"):
            sub.add_argument("--scene", required=name != "context")
        if name == "context":
            sub.add_argument("--topics", nargs="+", choices=("framing", "continuity", "motion", "optics", "blocking"))
            sub.add_argument("--compact", action="store_true",
                             help="Restore current scene and global decisions without full state/history bodies")
        if name in ("commit", "export"):
            sub.add_argument("--expected-revision", required=True, type=int)
            sub.add_argument("--expected-sha256", required=True)
        if name == "commit":
            sub.add_argument("--input", required=True)
            sub.add_argument("--amend", action="store_true")
            sub.add_argument("--change-reason")
        if name == "export":
            sub.add_argument("--text", required=True)
            sub.add_argument("--output", required=True, help="New JSON receipt including exact delivery text")
            sub.add_argument("--allow-unverified-geometry", action="store_true")
            sub.add_argument("--review-note")
    args = parser.parse_args(argv)
    try:
        root = project_root(args.project_root)
        output = {"init": initialize, "context": context, "commit": commit,
                  "check": check, "export": export}[args.command](args, root)
        print(json.dumps(output, ensure_ascii=False, allow_nan=False))
        return 0
    except GateError as exc:
        print(json.dumps({"ok": False, "error": exc.code, "message": exc.message,
                          "machine_constraints_only": True, "text_semantics_verified": False}, ensure_ascii=False))
        return 1
    except (OSError, ValueError, TypeError, KeyError, RecursionError, OverflowError) as exc:
        print(json.dumps({"ok": False, "error": "IO_OR_FORMAT_ERROR", "message": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
