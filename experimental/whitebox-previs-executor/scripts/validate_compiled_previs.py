#!/usr/bin/env python3
"""Validate a previs-compiler/1.0 contract before Blender execution."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("spec")
    value.add_argument("--output")
    return value


def number(value) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def vec(value, length: int) -> bool:
    return isinstance(value, list) and len(value) == length and all(number(item) for item in value)


def validate(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != "previs-compiler/1.0":
        errors.append("schema_version must be previs-compiler/1.0")

    playback = data.get("playback", {})
    fps = playback.get("fps")
    duration = playback.get("duration_s")
    resolution = playback.get("resolution")
    if not isinstance(fps, int) or fps <= 0:
        errors.append("playback.fps must be a positive integer")
    if not number(duration) or float(duration) <= 0:
        errors.append("playback.duration_s must be positive")
    if not vec(resolution, 2) or any(int(item) <= 0 for item in resolution or []):
        errors.append("playback.resolution must contain two positive numbers")

    geometry_ids: set[str] = set()
    for index, item in enumerate(data.get("scene", {}).get("geometry", [])):
        item_id = item.get("id")
        if not item_id or item_id in geometry_ids:
            errors.append(f"scene.geometry[{index}] has missing or duplicate id")
        geometry_ids.add(item_id)
        if item.get("proxy_type") not in {"grid_plane", "box"}:
            errors.append(f"scene.geometry[{index}] has unsupported proxy_type")
        if not vec(item.get("center"), 3):
            errors.append(f"scene.geometry[{index}].center must be a 3D vector")
        expected = 2 if item.get("proxy_type") == "grid_plane" else 3
        if not vec(item.get("size"), expected) or any(float(v) <= 0 for v in item.get("size", [])):
            errors.append(f"scene.geometry[{index}].size must contain {expected} positive numbers")

    actor_ids: set[str] = set()
    for index, actor in enumerate(data.get("cast", [])):
        actor_id = actor.get("id")
        if not actor_id or actor_id in actor_ids:
            errors.append(f"cast[{index}] has missing or duplicate id")
        actor_ids.add(actor_id)
        proxy_class = actor.get("proxy", {}).get("class")
        if proxy_class not in {"humanoid", "humanoid_mecha", "two_arm_hover", "two-arm-hover"}:
            errors.append(f"cast[{index}] has unsupported proxy class {proxy_class!r}")
        motion = actor.get("motion", [])
        if not motion:
            errors.append(f"cast[{index}] has no motion keys")
        prior = -math.inf
        for key_index, key in enumerate(motion):
            time_s = key.get("time_s")
            if not number(time_s) or float(time_s) < prior:
                errors.append(f"cast[{index}].motion[{key_index}] time is invalid or unsorted")
            elif number(duration) and not 0 <= float(time_s) <= float(duration):
                errors.append(f"cast[{index}].motion[{key_index}] lies outside playback")
            prior = float(time_s) if number(time_s) else prior
            if not vec(key.get("position"), 3):
                errors.append(f"cast[{index}].motion[{key_index}].position must be 3D")

    rigs = data.get("camera", {}).get("rigs", [])
    rig_ids: set[str] = set()
    for index, rig in enumerate(rigs):
        rig_id = rig.get("id")
        if not rig_id or rig_id in rig_ids:
            errors.append(f"camera.rigs[{index}] has missing or duplicate id")
        rig_ids.add(rig_id)
        keys = rig.get("keys", [])
        if len(keys) < 1:
            errors.append(f"camera.rigs[{index}] has no keys")
        prior = -math.inf
        for key_index, key in enumerate(keys):
            time_s = key.get("time_s")
            if not number(time_s) or float(time_s) < prior:
                errors.append(f"camera.rigs[{index}].keys[{key_index}] time is invalid or unsorted")
            elif number(duration) and not 0 <= float(time_s) <= float(duration):
                errors.append(f"camera.rigs[{index}].keys[{key_index}] lies outside playback")
            prior = float(time_s) if number(time_s) else prior
            if not vec(key.get("position"), 3) or not vec(key.get("look_at"), 3):
                errors.append(f"camera.rigs[{index}].keys[{key_index}] needs position and look_at 3D vectors")
            if not number(key.get("lens_mm")) or float(key.get("lens_mm", 0)) <= 0:
                errors.append(f"camera.rigs[{index}].keys[{key_index}].lens_mm must be positive")

    shots = data.get("timeline", {}).get("shots", [])
    if not shots:
        errors.append("timeline.shots must not be empty")
    cursor = 0.0
    shot_ids: set[str] = set()
    for index, shot in enumerate(shots):
        shot_id = shot.get("id")
        start = shot.get("start_s")
        end = shot.get("end_s")
        if not shot_id or shot_id in shot_ids:
            errors.append(f"timeline.shots[{index}] has missing or duplicate id")
        shot_ids.add(shot_id)
        if not number(start) or not number(end) or float(end) <= float(start):
            errors.append(f"timeline.shots[{index}] has invalid time range")
            continue
        if abs(float(start) - cursor) > 1e-6:
            errors.append(f"timeline.shots[{index}] creates a gap or overlap at {cursor:.6f}s")
        cursor = float(end)
        if shot.get("camera_id") not in rig_ids:
            errors.append(f"timeline.shots[{index}] references a missing camera")
    if number(duration) and abs(cursor - float(duration)) > 1e-6:
        errors.append("timeline shots do not cover the full playback duration")

    for index, tether in enumerate(data.get("tethers", [])):
        start = tether.get("start_s", tether.get("start"))
        end = tether.get("end_s", tether.get("end"))
        if not number(start) or not number(end) or float(end) <= float(start):
            errors.append(f"tethers[{index}] has an invalid active range")
        for endpoint_name in ("from", "to"):
            endpoint = tether.get(endpoint_name, {})
            if "actor" in endpoint and endpoint["actor"] not in actor_ids:
                errors.append(f"tethers[{index}].{endpoint_name} references a missing actor")
            if "world" in endpoint and not vec(endpoint["world"], 3):
                errors.append(f"tethers[{index}].{endpoint_name}.world must be a 3D vector")
            if "actor" not in endpoint and "world" not in endpoint:
                errors.append(f"tethers[{index}].{endpoint_name} needs actor or world")

    for index, effect in enumerate(data.get("effects", [])):
        effect_time = effect.get("time_s", effect.get("time"))
        if not number(effect_time) or (number(duration) and not 0 <= float(effect_time) <= float(duration)):
            errors.append(f"effects[{index}] has an invalid time")
        if not vec(effect.get("position"), 3):
            errors.append(f"effects[{index}].position must be a 3D vector")

    expected_frames = int(round(float(duration) * int(fps))) if number(duration) and isinstance(fps, int) else None
    validation_targets = data.get("validation_targets", {})
    action_required = bool(validation_targets.get("require_attack_block_contact_recoil_readability"))
    action_program = data.get("action_program")
    if action_required and not isinstance(action_program, dict):
        errors.append(
            "fight readability requires action_program; root motion and generic block poses are not an action backend"
        )
    if isinstance(action_program, dict):
        if action_program.get("schema_version") != "previs-action/1.0":
            errors.append("action_program.schema_version must be previs-action/1.0")
        if action_program.get("backend") != "baked_joint_ik":
            errors.append("action_program.backend must be baked_joint_ik")
        if data.get("meta", {}).get("execution_backend") != "rigged_joint_solver_v1":
            errors.append("action_program requires meta.execution_backend=rigged_joint_solver_v1")
        if not action_program.get("profile"):
            errors.append("action_program.profile is required")
        constraints = action_program.get("constraints", {})
        if len(constraints.get("weapon_grips", [])) != 2:
            errors.append("action_program.constraints.weapon_grips must contain primary and secondary hand")
        if not constraints.get("weapon_contact_socket"):
            errors.append("action_program.constraints.weapon_contact_socket is required")
        if len(constraints.get("defense_contact_sockets", [])) < 1:
            errors.append("action_program.constraints.defense_contact_sockets is required")
        if constraints.get("single_shared_contact") is not True:
            errors.append("action_program.constraints.single_shared_contact must be true")
        if constraints.get("no_root_only_fight") is not True:
            errors.append("action_program.constraints.no_root_only_fight must be true")

        beats = action_program.get("beats", [])
        if not beats:
            errors.append("action_program.beats must not be empty")
        else:
            expected_action_frame = 1
            for index, beat in enumerate(beats):
                start_frame = beat.get("start_frame")
                end_frame = beat.get("end_frame")
                if not isinstance(start_frame, int) or not isinstance(end_frame, int) or end_frame < start_frame:
                    errors.append(f"action_program.beats[{index}] has invalid frame range")
                    continue
                if start_frame != expected_action_frame:
                    errors.append(
                        f"action_program.beats[{index}] creates a gap or overlap at frame {expected_action_frame}"
                    )
                expected_action_frame = end_frame + 1
            if expected_frames is not None and expected_action_frame - 1 != expected_frames:
                errors.append("action_program beats do not cover the full playback frame range")

        contact_frame = action_program.get("contact_frame")
        hold_frames = action_program.get("hold_frames")
        if not isinstance(contact_frame, int) or contact_frame < 1:
            errors.append("action_program.contact_frame must be a positive integer")
        if not isinstance(hold_frames, int) or hold_frames < 1:
            errors.append("action_program.hold_frames must be a positive integer")
        if isinstance(contact_frame, int) and isinstance(hold_frames, int) and expected_frames is not None:
            if contact_frame + hold_frames - 1 > expected_frames:
                errors.append("action_program contact hold lies outside playback")

    unresolved = data.get("compile", {}).get("unresolved", [])
    if unresolved:
        warnings.append("compile.unresolved is not empty; output may only be called a diagnostic previs")

    return {
        "status": "pass" if not errors else "fail",
        "schema_version": data.get("schema_version"),
        "fps": fps,
        "duration_s": duration,
        "expected_frames": expected_frames,
        "shot_count": len(shots),
        "actor_count": len(actor_ids),
        "geometry_count": len(geometry_ids),
        "camera_count": len(rig_ids),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    args = parser().parse_args()
    source = Path(args.spec)
    result = validate(json.loads(source.read_text(encoding="utf-8")))
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
