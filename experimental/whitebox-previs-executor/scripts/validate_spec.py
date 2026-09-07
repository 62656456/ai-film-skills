#!/usr/bin/env python3
"""Validate whitebox previs specs before rendering."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def _vec3(value: object, where: str, errors: list[str]) -> None:
    if not isinstance(value, list) or len(value) != 3:
        errors.append(f"{where} must be a 3-number array")
        return
    if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in value):
        errors.append(f"{where} contains a non-finite number")


def validate(data: dict) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != "0.1":
        errors.append("schema_version must be '0.1'")

    fps = data.get("fps")
    if not isinstance(fps, int) or not 1 <= fps <= 120:
        errors.append("fps must be an integer from 1 to 120")

    resolution = data.get("resolution")
    if (
        not isinstance(resolution, list)
        or len(resolution) != 2
        or not all(isinstance(v, int) and 160 <= v <= 3840 for v in resolution)
    ):
        errors.append("resolution must be [width, height], each 160..3840")

    actors = data.get("actors", [])
    if not isinstance(actors, list):
        errors.append("actors must be an array")
        actors = []
    actor_ids: set[str] = set()
    allowed_actions = {"idle", "walk", "run", "turn", "sit", "reach", "dash", "guard", "slash", "slash_hold", "block", "thrust", "recoil"}
    for ai, actor in enumerate(actors):
        if not isinstance(actor, dict):
            errors.append(f"actors[{ai}] must be an object")
            continue
        actor_id = actor.get("id")
        if not isinstance(actor_id, str) or not actor_id:
            errors.append(f"actors[{ai}].id must be a non-empty string")
        elif actor_id in actor_ids:
            errors.append(f"duplicate actor id: {actor_id}")
        else:
            actor_ids.add(actor_id)
        rig = actor.get("rig", "humanoid")
        if rig not in {"humanoid", "two-arm-hover"}:
            errors.append(f"actor {actor_id or ai} uses unsupported rig: {rig}")
        keyframes = actor.get("keyframes", [])
        if not isinstance(keyframes, list) or not keyframes:
            errors.append(f"actor {actor_id or ai} needs keyframes")
            continue
        previous = -math.inf
        for ki, keyframe in enumerate(keyframes):
            if not isinstance(keyframe, dict):
                errors.append(f"actor {actor_id or ai} keyframe {ki} must be an object")
                continue
            time = keyframe.get("time")
            if not isinstance(time, (int, float)) or not math.isfinite(time):
                errors.append(f"actor {actor_id or ai} keyframe {ki} has invalid time")
            elif time < previous:
                errors.append(f"actor {actor_id or ai} keyframes are not time ordered")
            else:
                previous = time
            _vec3(keyframe.get("position"), f"actor {actor_id or ai} keyframe {ki}.position", errors)
            action = keyframe.get("action", "idle")
            if action not in allowed_actions:
                errors.append(f"actor {actor_id or ai} keyframe {ki} uses unsupported action: {action}")

    shots = data.get("shots", [])
    if not isinstance(shots, list) or not shots:
        errors.append("shots must be a non-empty array")
        shots = []
    previous_end = 0.0
    shot_ids: set[str] = set()
    for si, shot in enumerate(shots):
        if not isinstance(shot, dict):
            errors.append(f"shots[{si}] must be an object")
            continue
        shot_id = shot.get("id")
        if not isinstance(shot_id, str) or not shot_id:
            errors.append(f"shots[{si}].id must be a non-empty string")
            shot_id = str(si)
        elif shot_id in shot_ids:
            errors.append(f"duplicate shot id: {shot_id}")
        else:
            shot_ids.add(shot_id)
        start, end = shot.get("start"), shot.get("end")
        if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in (start, end)):
            errors.append(f"shot {shot_id} start/end must be finite numbers")
            continue
        if abs(start - previous_end) > 1e-6:
            errors.append(f"shot {shot_id} starts at {start}, expected {previous_end}")
        if end <= start:
            errors.append(f"shot {shot_id} end must be after start")
        previous_end = end
        camera_keys = shot.get("camera_keyframes", [])
        if not isinstance(camera_keys, list) or not camera_keys:
            errors.append(f"shot {shot_id} needs camera_keyframes")
            continue
        camera_previous = -math.inf
        for ki, keyframe in enumerate(camera_keys):
            if not isinstance(keyframe, dict):
                errors.append(f"shot {shot_id} camera keyframe {ki} must be an object")
                continue
            time = keyframe.get("time")
            if not isinstance(time, (int, float)) or not math.isfinite(time):
                errors.append(f"shot {shot_id} camera keyframe {ki} has invalid time")
            else:
                if time < start - 1e-6 or time > end + 1e-6:
                    errors.append(f"shot {shot_id} camera keyframe {ki} is outside the shot")
                if time < camera_previous:
                    errors.append(f"shot {shot_id} camera keyframes are not time ordered")
                camera_previous = time
            _vec3(keyframe.get("position"), f"shot {shot_id} camera {ki}.position", errors)
            _vec3(keyframe.get("look_at"), f"shot {shot_id} camera {ki}.look_at", errors)
            lens = keyframe.get("lens_mm", 35)
            if not isinstance(lens, (int, float)) or not 8 <= lens <= 300:
                errors.append(f"shot {shot_id} camera {ki}.lens_mm must be 8..300")
        if camera_keys and abs(camera_keys[0].get("time", start) - start) > 1e-6:
            warnings.append(f"shot {shot_id} first camera keyframe does not start at shot boundary")
        if camera_keys and abs(camera_keys[-1].get("time", end) - end) > 1e-6:
            warnings.append(f"shot {shot_id} last camera keyframe does not end at shot boundary")

    sequence_end = previous_end if shots else 0.0
    for actor in actors:
        if not isinstance(actor, dict) or not actor.get("keyframes"):
            continue
        actor_id = actor.get("id", "unknown")
        keys = actor["keyframes"]
        if keys[0].get("time", 0) > 0:
            warnings.append(f"actor {actor_id} has no keyframe at sequence start")
        if keys[-1].get("time", 0) < sequence_end:
            warnings.append(f"actor {actor_id} has no keyframe at sequence end")

    effects = data.get("effects", [])
    if not isinstance(effects, list):
        errors.append("effects must be an array")
    else:
        for ei, effect in enumerate(effects):
            if not isinstance(effect, dict) or effect.get("type") != "impact":
                errors.append(f"effects[{ei}] must be an impact object")
                continue
            effect_time = effect.get("time")
            if not isinstance(effect_time, (int, float)) or not 0 <= effect_time <= sequence_end:
                errors.append(f"effects[{ei}].time is outside the sequence")
            _vec3(effect.get("position"), f"effects[{ei}].position", errors)

    tethers = data.get("tethers", [])
    if not isinstance(tethers, list):
        errors.append("tethers must be an array")
    else:
        for ti, tether in enumerate(tethers):
            if not isinstance(tether, dict):
                errors.append(f"tethers[{ti}] must be an object")
                continue
            start, end = tether.get("start"), tether.get("end")
            if not all(isinstance(v, (int, float)) for v in (start, end)) or start < 0 or end <= start or end > sequence_end:
                errors.append(f"tethers[{ti}] has invalid start/end")
            for endpoint_name in ("from", "to"):
                endpoint = tether.get(endpoint_name, {})
                if not isinstance(endpoint, dict):
                    errors.append(f"tethers[{ti}].{endpoint_name} must be an object")
                    continue
                if "actor" in endpoint:
                    if endpoint["actor"] not in actor_ids:
                        errors.append(f"tethers[{ti}].{endpoint_name} references unknown actor")
                    _vec3(endpoint.get("offset", [0, 0, 0]), f"tethers[{ti}].{endpoint_name}.offset", errors)
                elif "world" in endpoint:
                    _vec3(endpoint["world"], f"tethers[{ti}].{endpoint_name}.world", errors)
                else:
                    errors.append(f"tethers[{ti}].{endpoint_name} needs actor or world")

    return {
        "ready": not errors,
        "errors": errors,
        "warnings": warnings,
        "actor_count": len(actors),
        "shot_count": len(shots),
        "duration_seconds": sequence_end,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.spec.read_text(encoding="utf-8"))
    result = validate(data)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["ready"] else 2


if __name__ == "__main__":
    sys.exit(main())
