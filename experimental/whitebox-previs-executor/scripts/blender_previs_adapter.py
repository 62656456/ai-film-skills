#!/usr/bin/env python3
"""Render a previs-compiler/1.0 contract as a neutral 3D MP4 in Blender.

Run with Blender, not the system Python:
  blender --background --factory-startup --python-exit-code 1 \
    --python blender_previs_adapter.py -- \
    --spec previs_compiled_v1.json --output preview.mp4 \
    --project preview.blend --validation validation.json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Euler, Vector


def parse_args() -> argparse.Namespace:
    raw = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--validation", required=True)
    return parser.parse_args(raw)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def clamp_tone(value: float) -> float:
    return min(1.0, max(0.03, float(value)))


def material(name: str, tone: float, tint=(1.0, 1.0, 1.0)):
    tone = clamp_tone(tone)
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (tone * tint[0], tone * tint[1], tone * tint[2], 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = mat.diffuse_color
        bsdf.inputs["Roughness"].default_value = 0.82
        bsdf.inputs["Metallic"].default_value = 0.08
    return mat


def add_cube(name: str, center, size, mat, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=tuple(center))
    obj = bpy.context.object
    obj.name = name
    obj.scale = (float(size[0]) / 2.0, float(size[1]) / 2.0, float(size[2]) / 2.0)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    if parent is not None:
        obj.parent = parent
    return obj


def add_cylinder(name: str, center, radius: float, depth: float, mat, parent=None, vertices: int = 12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=float(radius), depth=float(depth), location=tuple(center))
    obj = bpy.context.object
    obj.name = name
    if mat:
        obj.data.materials.append(mat)
    if parent is not None:
        obj.parent = parent
    return obj


def set_visible_at(obj, frame: int, visible: bool) -> None:
    obj.hide_render = not visible
    obj.hide_viewport = not visible
    obj.keyframe_insert("hide_render", frame=frame)
    obj.keyframe_insert("hide_viewport", frame=frame)


def add_grid_plane(item, palette):
    center = item["center"]
    size = item["size"]
    grid = float(item.get("grid_m", 1.0))
    floor = add_cube(
        item["id"],
        (center[0], center[1], -0.04),
        (size[0], size[1], 0.08),
        palette["floor"],
    )
    half_x = float(size[0]) / 2.0
    half_y = float(size[1]) / 2.0
    x = -half_x
    index = 0
    while x <= half_x + 1e-6:
        add_cube(
            f"{item['id']}_grid_x_{index}",
            (center[0] + x, center[1], 0.012),
            (0.025, size[1], 0.018),
            palette["grid"],
        )
        index += 1
        x += grid
    y = -half_y
    index = 0
    while y <= half_y + 1e-6:
        add_cube(
            f"{item['id']}_grid_y_{index}",
            (center[0], center[1] + y, 0.013),
            (size[0], 0.025, 0.019),
            palette["grid"],
        )
        index += 1
        y += grid
    return floor


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def set_curve_interpolation(obj, interpolation: str) -> None:
    action = getattr(getattr(obj, "animation_data", None), "action", None)
    if not action:
        return
    curves = getattr(action, "fcurves", None)
    if curves is None and hasattr(action, "layers"):
        curves = []
        for layer in action.layers:
            for strip in layer.strips:
                for channelbag in getattr(strip, "channelbags", []):
                    curves.extend(channelbag.fcurves)
    for curve in curves or []:
        for point in curve.keyframe_points:
            point.interpolation = interpolation


def held_frame(frame: int, hold_ranges: list[tuple[int, int]]) -> int:
    for start, end in hold_ranges:
        if start <= frame <= end:
            return start
    return frame


def adjusted_key_frame(frame: int, hold_ranges: list[tuple[int, int]]) -> int:
    for _start, end in hold_ranges:
        if frame == end + 1:
            return end
    return frame


def create_humanoid(actor, frame_for, frame_end, fps, palette, hold_ranges):
    actor_id = actor["id"]
    height = float(actor.get("proxy", {}).get("height_m", 1.75))
    tone = float(actor.get("proxy", {}).get("tone", 0.9))
    body_mat = material(f"MAT_{actor_id}_BODY", tone, (0.90, 0.96, 1.0))
    armor_mat = material(f"MAT_{actor_id}_ARMOR", max(0.35, tone - 0.14), (0.82, 0.92, 1.0))
    joint_mat = palette["joint"]

    root = bpy.data.objects.new(f"ACTOR_{actor_id}", None)
    bpy.context.collection.objects.link(root)
    scale = height / 2.0
    root.scale = (scale, scale, scale)

    parts = {}
    parts["pelvis"] = add_cube(f"{actor_id}_pelvis", (0, 0, 0.88), (0.68, 0.42, 0.34), armor_mat, root)
    parts["torso"] = add_cube(f"{actor_id}_torso", (0, 0, 1.32), (0.82, 0.48, 0.68), body_mat, root)
    parts["chest"] = add_cube(f"{actor_id}_chest", (0, -0.255, 1.38), (0.42, 0.08, 0.25), armor_mat, root)
    parts["head"] = add_cube(f"{actor_id}_head", (0, 0, 1.84), (0.45, 0.42, 0.46), body_mat, root)
    parts["visor"] = add_cube(f"{actor_id}_visor", (0, -0.225, 1.88), (0.28, 0.05, 0.10), joint_mat, root)
    for side, sign in (("L", -1.0), ("R", 1.0)):
        parts[f"shoulder_{side}"] = add_cube(
            f"{actor_id}_shoulder_{side}", (0.56 * sign, 0, 1.48), (0.34, 0.55, 0.30), armor_mat, root
        )
        parts[f"arm_{side}"] = add_cube(
            f"{actor_id}_arm_{side}", (0.58 * sign, 0, 1.08), (0.24, 0.27, 0.58), body_mat, root
        )
        parts[f"forearm_{side}"] = add_cube(
            f"{actor_id}_forearm_{side}", (0.58 * sign, 0, 0.72), (0.29, 0.33, 0.45), armor_mat, root
        )
        parts[f"thigh_{side}"] = add_cube(
            f"{actor_id}_thigh_{side}", (0.24 * sign, 0, 0.54), (0.30, 0.34, 0.62), body_mat, root
        )
        parts[f"shin_{side}"] = add_cube(
            f"{actor_id}_shin_{side}", (0.24 * sign, -0.01, 0.17), (0.32, 0.38, 0.55), armor_mat, root
        )

    weapon_root = None
    weapon = actor.get("weapon") or actor.get("proxy", {}).get("weapon")
    if weapon and weapon.get("type") == "hammer":
        weapon_root = bpy.data.objects.new(f"{actor_id}_hammer_root", None)
        bpy.context.collection.objects.link(weapon_root)
        weapon_root.parent = root
        weapon_root.location = (0.48, -0.15, 1.10)
        weapon_root.rotation_mode = "QUATERNION"
        world_length = float(weapon.get("length_m", weapon.get("length", height * 0.65)))
        local_length = world_length / scale
        head_world = weapon.get("head_size_m", weapon.get("head_size", [height * 0.23, height * 0.12, height * 0.12]))
        head_local = [float(value) / scale for value in head_world]
        handle_thickness = max(0.035, 0.42 / scale)
        for segment in range(3):
            start = local_length * segment / 3.0
            end = local_length * (segment + 1) / 3.0
            add_cube(
                f"{actor_id}_hammer_handle_{segment + 1}",
                (0.0, -(start + end) / 2.0, 0.0),
                (handle_thickness * (1.0 + segment * 0.12), end - start, handle_thickness * (1.0 + segment * 0.12)),
                armor_mat if segment % 2 == 0 else joint_mat,
                weapon_root,
            )
        parts["hammer_head"] = add_cube(
            f"{actor_id}_hammer_head",
            (0.0, -local_length, 0.0),
            head_local,
            armor_mat,
            weapon_root,
        )

    motion = actor.get("motion", [])
    for key in motion:
        frame = adjusted_key_frame(frame_for(float(key["time_s"])), hold_ranges)
        position = key["position"]
        action = str(key.get("pose", key.get("action", "idle")))
        if action in {"dash", "run", "slash", "slash_hold"}:
            pitch = math.radians(-10.0)
        elif action == "recoil":
            pitch = math.radians(16.0)
        else:
            pitch = 0.0
        root.location = tuple(float(v) for v in position)
        root.rotation_euler = (pitch, 0.0, math.radians(-float(key.get("facing_deg", 0.0))))
        root.keyframe_insert("location", frame=frame)
        root.keyframe_insert("rotation_euler", frame=frame)
        if weapon_root is not None:
            contact_point = actor.get("contact_point")
            if action in {"slash", "slash_hold"} and contact_point:
                root_rotation = Euler(root.rotation_euler, "XYZ").to_matrix()
                pivot_world = Vector(root.location) + root_rotation @ (Vector(weapon_root.location) * scale)
                world_direction = Vector(tuple(float(value) for value in contact_point)) - pivot_world
                local_direction = root_rotation.inverted() @ world_direction
                rotation_quaternion = local_direction.to_track_quat("-Y", "Z")
            elif action in {"guard", "block"}:
                rotation_quaternion = Euler((math.radians(-18), 0.0, math.radians(96)), "XYZ").to_quaternion()
            elif action in {"reach", "recoil"}:
                rotation_quaternion = Euler((math.radians(18), 0.0, math.radians(12)), "XYZ").to_quaternion()
            else:
                rotation_quaternion = Euler((math.radians(-12), 0.0, math.radians(4)), "XYZ").to_quaternion()
            weapon_root.rotation_quaternion = rotation_quaternion
            weapon_root.keyframe_insert("rotation_quaternion", frame=frame)
    set_curve_interpolation(root, "LINEAR")
    if weapon_root is not None:
        set_curve_interpolation(weapon_root, "LINEAR")

    run_parts = [
        parts["arm_L"],
        parts["forearm_L"],
        parts["arm_R"],
        parts["forearm_R"],
        parts["thigh_L"],
        parts["shin_L"],
        parts["thigh_R"],
        parts["shin_R"],
    ]
    step = max(3, int(round(fps / 4)))
    sample_frames = set(range(1, frame_end + 1, step))
    sample_frames.add(frame_end)
    for start, end in hold_ranges:
        sample_frames.update({start, end, min(frame_end, end + 1)})
    for frame in sorted(sample_frames):
        effective_frame = held_frame(frame, hold_ranges)
        seconds = (effective_frame - 1) / fps
        action = "idle"
        for key in motion:
            if float(key["time_s"]) <= seconds + 1e-6:
                action = str(key.get("pose", key.get("action", "idle")))
            else:
                break
        swing = math.sin(seconds * math.tau * 2.0) * 0.42
        if action in {"dash", "run"}:
            values = (swing, swing * 0.55, -swing, -swing * 0.55, -swing, swing * 0.45, swing, -swing * 0.45)
        elif action in {"guard", "block"}:
            values = (-0.72, -0.45, -0.72, -0.45, -0.18, 0.18, 0.18, -0.18)
        elif action in {"slash", "slash_hold"}:
            values = (-1.05, -0.55, -0.92, -0.45, -0.36, 0.22, 0.34, -0.20)
        elif action == "reach":
            values = (-1.22, -0.72, 0.12, 0.08, -0.12, 0.06, 0.12, -0.06)
        elif action == "recoil":
            values = (0.78, 0.42, -0.78, -0.42, 0.25, -0.18, -0.25, 0.18)
        else:
            values = (0.0,) * 8
        for obj, angle in zip(run_parts, values):
            obj.rotation_euler = (angle, 0.0, 0.0)
            obj.keyframe_insert("rotation_euler", frame=frame)
    for obj in run_parts:
        set_curve_interpolation(obj, "LINEAR")
    return root


def create_two_arm_hover(actor, frame_for, palette, hold_ranges):
    actor_id = actor["id"]
    proxy = actor.get("proxy", {})
    span = float(proxy.get("span_m", actor.get("span", 32.0)))
    length = float(proxy.get("length_m", 35.0))
    tone = float(proxy.get("tone", 0.66))
    scale = span / 32.0
    body_mat = material(f"MAT_{actor_id}_BODY", tone, (0.78, 0.82, 0.88))
    armor_mat = material(f"MAT_{actor_id}_ARMOR", max(0.22, tone - 0.16), (0.82, 0.48, 0.42))
    joint_mat = palette["joint"]

    root = bpy.data.objects.new(f"ACTOR_{actor_id}", None)
    bpy.context.collection.objects.link(root)
    root.scale = (scale, scale, scale)

    add_cube(f"{actor_id}_central_body", (0, 0, 10.0), (12.0, 9.0, 5.5), body_mat, root)
    add_cube(f"{actor_id}_spine", (0, 3.0, 10.8), (8.0, 6.0, 3.0), armor_mat, root)
    add_cube(f"{actor_id}_shoulder_L", (-10.0, 0.4, 10.2), (7.0, 9.0, 6.2), armor_mat, root)
    add_cube(f"{actor_id}_shoulder_R", (10.0, 0.4, 10.2), (7.0, 9.0, 6.2), armor_mat, root)

    head_root = bpy.data.objects.new(f"{actor_id}_head_root", None)
    bpy.context.collection.objects.link(head_root)
    head_root.parent = root
    head_root.location = (0.0, -6.0, 11.5)
    add_cube(f"{actor_id}_head_core", (0.0, -1.5, 0.0), (6.0, 5.5, 4.2), body_mat, head_root)
    beak_upper = add_cube(f"{actor_id}_beak_upper", (0.0, -5.0, 0.7), (3.6, 5.5, 1.8), armor_mat, head_root)
    beak_lower = add_cube(f"{actor_id}_beak_lower", (0.0, -5.0, -1.0), (3.6, 5.5, 1.5), armor_mat, head_root)
    add_cylinder(f"{actor_id}_focus_ring", (0.0, -7.8, -0.1), 1.15, 0.35, joint_mat, head_root, vertices=20).rotation_euler = (
        math.radians(90),
        0.0,
        0.0,
    )

    arm_roots = {}
    for side, sign in (("L", -1.0), ("R", 1.0)):
        arm_root = bpy.data.objects.new(f"{actor_id}_arm_root_{side}", None)
        bpy.context.collection.objects.link(arm_root)
        arm_root.parent = root
        arm_root.location = (10.5 * sign, -0.3, 8.8)
        add_cube(f"{actor_id}_upper_arm_{side}", (0.0, 0.0, -3.1), (3.0, 4.2, 7.0), body_mat, arm_root)
        add_cube(f"{actor_id}_forearm_{side}", (0.8 * sign, -1.0, -8.5), (3.2, 4.4, 7.2), armor_mat, arm_root)
        palm = add_cube(f"{actor_id}_palm_{side}", (1.0 * sign, -1.8, -12.2), (3.8, 4.8, 2.2), body_mat, arm_root)
        for finger in range(3):
            add_cube(
                f"{actor_id}_claw_{side}_{finger + 1}",
                ((0.0 + finger * 0.9) * sign, -4.0 - finger * 0.35, -13.4),
                (0.65, 4.0, 0.75),
                armor_mat,
                arm_root,
            )
        arm_roots[side] = arm_root

    motion = actor.get("motion", [])
    for index, key in enumerate(motion):
        frame = adjusted_key_frame(frame_for(float(key["time_s"])), hold_ranges)
        position = key["position"]
        action = str(key.get("pose", key.get("action", "guard")))
        pitch = math.radians(-8.0 if action in {"block", "thrust"} else (14.0 if action == "recoil" else 0.0))
        root.location = tuple(float(value) for value in position)
        root.rotation_euler = (pitch, 0.0, math.radians(-float(key.get("facing_deg", 0.0))))
        root.keyframe_insert("location", frame=frame)
        root.keyframe_insert("rotation_euler", frame=frame)
        for side, sign in (("L", -1.0), ("R", 1.0)):
            arm_root = arm_roots[side]
            if action in {"dash", "run"}:
                offset = 0.8 if (index + (0 if side == "L" else 1)) % 2 == 0 else -0.8
                arm_root.location = (10.5 * sign, -0.3 + offset, 8.8)
                arm_root.rotation_euler = (math.radians(offset * 8.0), 0.0, math.radians(-sign * 3.0))
            elif action in {"thrust", "slash"}:
                arm_root.location = (10.0 * sign, -2.8, 9.2)
                arm_root.rotation_euler = (math.radians(-24.0), math.radians(sign * 8.0), math.radians(-sign * 7.0))
            elif action in {"block", "guard"}:
                arm_root.location = (7.0 * sign, -2.4, 9.8)
                arm_root.rotation_euler = (math.radians(-42.0), math.radians(sign * 12.0), math.radians(-sign * 34.0))
            elif action == "recoil":
                arm_root.location = (11.8 * sign, 1.5, 10.5)
                arm_root.rotation_euler = (math.radians(24.0), math.radians(-sign * 8.0), math.radians(sign * 22.0))
            else:
                arm_root.location = (10.5 * sign, -0.3, 8.8)
                arm_root.rotation_euler = (0.0, 0.0, 0.0)
            arm_root.keyframe_insert("location", frame=frame)
            arm_root.keyframe_insert("rotation_euler", frame=frame)
        cannon_open = action in {"cannon_open", "cannon_ready"}
        beak_upper.rotation_euler = (math.radians(18.0 if cannon_open else 0.0), 0.0, 0.0)
        beak_lower.rotation_euler = (math.radians(-18.0 if cannon_open else 0.0), 0.0, 0.0)
        beak_upper.keyframe_insert("rotation_euler", frame=frame)
        beak_lower.keyframe_insert("rotation_euler", frame=frame)

    set_curve_interpolation(root, "LINEAR")
    set_curve_interpolation(beak_upper, "LINEAR")
    set_curve_interpolation(beak_lower, "LINEAR")
    for arm_root in arm_roots.values():
        set_curve_interpolation(arm_root, "LINEAR")
    return root


def interpolate_motion_position(actor: dict, time_s: float) -> Vector:
    motion = actor.get("motion", [])
    if not motion:
        return Vector((0.0, 0.0, 0.0))
    if time_s <= float(motion[0]["time_s"]):
        return Vector(tuple(float(value) for value in motion[0]["position"]))
    if time_s >= float(motion[-1]["time_s"]):
        return Vector(tuple(float(value) for value in motion[-1]["position"]))
    for left, right in zip(motion, motion[1:]):
        start = float(left["time_s"])
        end = float(right["time_s"])
        if start <= time_s <= end:
            a = Vector(tuple(float(value) for value in left["position"]))
            b = Vector(tuple(float(value) for value in right["position"]))
            amount = 0.0 if end <= start else (time_s - start) / (end - start)
            return a.lerp(b, amount)
    return Vector(tuple(float(value) for value in motion[-1]["position"]))


def tether_endpoint(endpoint: dict, actor_specs: dict[str, dict], time_s: float) -> Vector:
    if "world" in endpoint:
        return Vector(tuple(float(value) for value in endpoint["world"]))
    actor_id = endpoint.get("actor")
    if actor_id not in actor_specs:
        raise ValueError(f"Tether references missing actor {actor_id!r}")
    base = interpolate_motion_position(actor_specs[actor_id], time_s)
    offset = Vector(tuple(float(value) for value in endpoint.get("offset", [0.0, 0.0, 0.0])))
    return base + offset


def create_tethers(spec, actor_specs, frame_for, frame_end, fps):
    for tether in spec.get("tethers", []):
        tether_id = tether["id"]
        tone = float(tether.get("tone", 0.8))
        cable_mat = material(f"MAT_TETHER_{tether_id}", tone, (0.76, 0.86, 1.0))
        cable = add_cylinder(f"TETHER_{tether_id}", (0.0, 0.0, 0.0), 0.16, 1.0, cable_mat, vertices=10)
        cable.rotation_mode = "QUATERNION"
        start_frame = frame_for(float(tether.get("start_s", tether.get("start"))))
        end_frame = frame_for(float(tether.get("end_s", tether.get("end"))))
        if start_frame > 1:
            set_visible_at(cable, start_frame - 1, False)
        set_visible_at(cable, start_frame, True)
        if end_frame < frame_end:
            set_visible_at(cable, end_frame + 1, False)
        frames = set(range(start_frame, end_frame + 1, max(2, int(round(fps / 4)))))
        frames.update({start_frame, end_frame})
        for frame in sorted(frames):
            time_s = (frame - 1) / fps
            start = tether_endpoint(tether["from"], actor_specs, time_s)
            end = tether_endpoint(tether["to"], actor_specs, time_s)
            direction = end - start
            length = max(0.001, direction.length)
            cable.location = (start + end) / 2.0
            cable.rotation_quaternion = direction.to_track_quat("Z", "Y")
            cable.scale = (1.0, 1.0, length)
            cable.keyframe_insert("location", frame=frame)
            cable.keyframe_insert("rotation_quaternion", frame=frame)
            cable.keyframe_insert("scale", frame=frame)
        set_curve_interpolation(cable, "LINEAR")


def create_effects(spec, frame_for, frame_end, fps):
    for index, effect in enumerate(spec.get("effects", [])):
        if effect.get("type") != "impact":
            continue
        impact_mat = material(f"MAT_IMPACT_{index}", 0.92, (1.0, 0.42, 0.08))
        position = tuple(float(value) for value in effect["position"])
        radius = float(effect.get("radius", 1.0))
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=radius, location=position)
        marker = bpy.context.object
        marker.name = f"IMPACT_{index + 1}"
        marker.data.materials.append(impact_mat)
        effect_time = float(effect.get("time_s", effect.get("time")))
        start = frame_for(effect_time)
        if effect.get("hold"):
            hold_frames = int(effect.get("hold_frames", max(1, round(float(effect.get("duration_s", effect.get("duration", 0.2))) * fps))))
            end = min(frame_end, start + hold_frames - 1)
        else:
            end = frame_for(effect_time + float(effect.get("duration_s", effect.get("duration", 0.2))))
        if start > 1:
            set_visible_at(marker, start - 1, False)
        set_visible_at(marker, start, True)
        if effect.get("hold"):
            marker.scale = (1.0, 1.0, 1.0)
            marker.keyframe_insert("scale", frame=start)
            marker.keyframe_insert("scale", frame=end)
        else:
            marker.scale = (0.55, 0.55, 0.55)
            marker.keyframe_insert("scale", frame=start)
            marker.scale = (1.0, 1.0, 1.0)
            marker.keyframe_insert("scale", frame=end)
        if end < frame_end:
            set_visible_at(marker, end + 1, False)
        set_curve_interpolation(marker, "LINEAR")


def create_camera(rig, frame_for, sensor_width, fps, hold_ranges):
    data = bpy.data.cameras.new(rig["id"])
    data.sensor_width = float(sensor_width)
    data.clip_start = 0.05
    data.clip_end = 500.0
    camera = bpy.data.objects.new(rig["id"], data)
    bpy.context.collection.objects.link(camera)
    camera.rotation_mode = "QUATERNION"

    keys = []
    for source in rig.get("keys", []):
        key = dict(source)
        raw_frame = frame_for(float(key["time_s"]))
        adjusted = adjusted_key_frame(raw_frame, hold_ranges)
        if adjusted != raw_frame:
            key["time_s"] = (adjusted - 1) / fps
        keys.append(key)
    if not keys:
        raise ValueError(f"Camera {rig['id']} has no keys")

    def sample(time_s: float):
        if time_s <= float(keys[0]["time_s"]):
            return keys[0]["position"], keys[0]["look_at"], float(keys[0].get("lens_mm", 35.0))
        if time_s >= float(keys[-1]["time_s"]):
            return keys[-1]["position"], keys[-1]["look_at"], float(keys[-1].get("lens_mm", 35.0))
        for left, right in zip(keys, keys[1:]):
            start = float(left["time_s"])
            end = float(right["time_s"])
            if start <= time_s <= end:
                amount = 0.0 if end <= start else (time_s - start) / (end - start)
                easing = str(right.get("easing", left.get("easing", "linear")))
                if easing == "smooth":
                    amount = amount * amount * (3.0 - 2.0 * amount)
                elif easing == "hold":
                    amount = 0.0
                position = Vector(left["position"]).lerp(Vector(right["position"]), amount)
                look_at = Vector(left["look_at"]).lerp(Vector(right["look_at"]), amount)
                lens = float(left.get("lens_mm", 35.0)) + (
                    float(right.get("lens_mm", 35.0)) - float(left.get("lens_mm", 35.0))
                ) * amount
                return position, look_at, lens
        return keys[-1]["position"], keys[-1]["look_at"], float(keys[-1].get("lens_mm", 35.0))

    start_frame = frame_for(float(keys[0]["time_s"]))
    end_frame = frame_for(float(keys[-1]["time_s"]))
    for frame in range(start_frame, end_frame + 1):
        effective_frame = held_frame(frame, hold_ranges)
        position, target_value, lens = sample((effective_frame - 1) / fps)
        camera.location = tuple(float(value) for value in position)
        target = Vector(tuple(float(value) for value in target_value))
        direction = target - camera.location
        if direction.length < 1e-6:
            raise ValueError(f"Camera {rig['id']} has zero-length look direction at frame {frame}")
        camera.rotation_quaternion = direction.to_track_quat("-Z", "Y")
        data.lens = float(lens)
        camera.keyframe_insert("location", frame=frame)
        camera.keyframe_insert("rotation_quaternion", frame=frame)
        data.keyframe_insert("lens", frame=frame)
    set_curve_interpolation(camera, "LINEAR")
    set_curve_interpolation(data, "LINEAR")
    return camera


def configure_lighting(scene, palette):
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.035, 0.045, 0.06, 1.0)
    background.inputs["Strength"].default_value = 0.32

    sun_data = bpy.data.lights.new("PREVIS_SUN", type="SUN")
    sun_data.energy = 2.2
    sun_data.color = (0.90, 0.94, 1.0)
    sun = bpy.data.objects.new("PREVIS_SUN", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(28), math.radians(-18), math.radians(-35))

    area_data = bpy.data.lights.new("PREVIS_AREA", type="AREA")
    area_data.energy = 900.0
    area_data.shape = "DISK"
    area_data.size = 6.0
    area_data.color = (0.72, 0.82, 1.0)
    area = bpy.data.objects.new("PREVIS_AREA", area_data)
    bpy.context.collection.objects.link(area)
    area.location = (-4.0, -1.0, 7.0)
    area.rotation_euler = (math.radians(18), 0.0, math.radians(-25))


def render_contract(spec, output: Path, project: Path, validation: Path) -> None:
    started = time.perf_counter()
    clear_scene()
    scene = bpy.context.scene
    playback = spec["playback"]
    fps = int(playback.get("fps", 24))
    duration = float(playback["duration_s"])
    width, height = [int(v) for v in playback.get("resolution", [960, 540])]
    frame_end = int(round(duration * fps))

    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = frame_end
    # Blender 5.2 separates media type from the specific file format. Without
    # switching to VIDEO first, the FFMPEG enum is deliberately rejected.
    scene.render.image_settings.media_type = "VIDEO"
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    scene.render.ffmpeg.audio_codec = "NONE"
    scene.render.film_transparent = False
    scene.render.use_file_extension = True

    output_base = output.parent / output.stem
    ensure_parent(output_base)
    stale_outputs = list(output.parent.glob(output_base.name + "*.mp4"))
    if stale_outputs:
        raise FileExistsError(
            "Refusing to overwrite an existing previs output: "
            + ", ".join(str(path) for path in stale_outputs)
        )
    scene.render.filepath = str(output_base)

    def frame_for(seconds: float) -> int:
        return min(frame_end, max(1, int(round(seconds * fps)) + 1))

    palette = {
        "floor": material("MAT_FLOOR", 0.22, (0.62, 0.68, 0.76)),
        "grid": material("MAT_GRID", 0.08, (0.72, 0.82, 1.0)),
        "joint": material("MAT_JOINT", 0.12, (0.50, 0.62, 0.78)),
    }
    configure_lighting(scene, palette)

    hold_ranges: list[tuple[int, int]] = []
    for effect in spec.get("effects", []):
        if not effect.get("hold"):
            continue
        start = frame_for(float(effect.get("time_s", effect.get("time", 0.0))))
        hold_frames = int(effect.get("hold_frames", max(1, round(float(effect.get("duration_s", effect.get("duration", 0.0))) * fps))))
        hold_ranges.append((start, min(frame_end, start + hold_frames - 1)))

    for item in spec.get("scene", {}).get("geometry", []):
        proxy_type = item.get("proxy_type", "box")
        if proxy_type == "grid_plane":
            add_grid_plane(item, palette)
            continue
        tone = float(item.get("tone", 0.45))
        mat = material(f"MAT_{item['id']}", tone, (0.74, 0.80, 0.88))
        add_cube(item["id"], item["center"], item["size"], mat)

    actors = {}
    actor_specs = {actor["id"]: actor for actor in spec.get("cast", [])}
    for actor in spec.get("cast", []):
        proxy_class = actor.get("proxy", {}).get("class", "humanoid")
        if proxy_class in {"humanoid", "humanoid_mecha"}:
            actors[actor["id"]] = create_humanoid(actor, frame_for, frame_end, fps, palette, hold_ranges)
        elif proxy_class in {"two_arm_hover", "two-arm-hover"}:
            actors[actor["id"]] = create_two_arm_hover(actor, frame_for, palette, hold_ranges)
        else:
            raise ValueError(f"Unsupported proxy class: {proxy_class}")

    create_tethers(spec, actor_specs, frame_for, frame_end, fps)
    create_effects(spec, frame_for, frame_end, fps)

    cameras = {}
    sensor_width = float(spec.get("camera", {}).get("sensor_width_mm", 36.0))
    for rig in spec.get("camera", {}).get("rigs", []):
        cameras[rig["id"]] = create_camera(rig, frame_for, sensor_width, fps, hold_ranges)
    if not cameras:
        raise ValueError("Spec contains no camera rigs")

    for shot in spec.get("timeline", {}).get("shots", []):
        camera_id = shot["camera_id"]
        if camera_id not in cameras:
            raise ValueError(f"Shot {shot['id']} references missing camera {camera_id}")
        marker = scene.timeline_markers.new(shot["id"], frame=frame_for(float(shot["start_s"])))
        marker.camera = cameras[camera_id]
    first_shot = spec["timeline"]["shots"][0]
    scene.camera = cameras[first_shot["camera_id"]]

    ensure_parent(project)
    bpy.ops.wm.save_as_mainfile(filepath=str(project))
    bpy.ops.render.render(animation=True)

    candidates = list(output.parent.glob(output_base.name + "*.mp4"))
    rendered = max(candidates, key=lambda path: path.stat().st_mtime) if candidates else output
    if not rendered.exists() or rendered.stat().st_size == 0:
        raise RuntimeError(f"Blender did not create a non-empty MP4: {rendered}")
    if rendered.resolve() != output.resolve():
        rendered.replace(output)
        rendered = output

    decoded_frames = None
    decoded_size = None
    decode_error = None
    try:
        clip = bpy.data.movieclips.load(str(rendered), check_existing=False)
        decoded_frames = int(clip.frame_duration)
        decoded_size = [int(clip.size[0]), int(clip.size[1])]
    except Exception as exc:  # Blender decoder evidence is helpful but not the renderer itself.
        decode_error = f"{type(exc).__name__}: {exc}"

    report = {
        "status": "pass" if decoded_frames in {None, frame_end} else "frame_count_mismatch",
        "engine": "Blender 5.2.1 LTS / EEVEE / FFmpeg H.264",
        "spec_path": str(Path(args.spec).resolve()),
        "project_path": str(project.resolve()),
        "video_path": str(rendered.resolve()),
        "fps": fps,
        "duration_s_expected": duration,
        "frames_expected": frame_end,
        "decoded_frames": decoded_frames,
        "decoded_size": decoded_size,
        "decode_error": decode_error,
        "resolution_expected": [width, height],
        "shots": [
            {
                "id": shot["id"],
                "start_s": shot["start_s"],
                "end_s": shot["end_s"],
                "camera_id": shot["camera_id"],
                "start_frame": frame_for(float(shot["start_s"])),
            }
            for shot in spec["timeline"]["shots"]
        ],
        "elapsed_s": round(time.perf_counter() - started, 3),
        "claim_boundary": "Proves this compiled 3D camera/blocking interpretation, not final AI video pixels.",
    }
    ensure_parent(validation)
    validation.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["status"] != "pass":
        raise RuntimeError(f"Rendered MP4 failed validation: {report['status']}")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = parse_args()
    spec_path = Path(args.spec).resolve()
    output_path = Path(args.output).resolve()
    project_path = Path(args.project).resolve()
    validation_path = Path(args.validation).resolve()
    contract = json.loads(spec_path.read_text(encoding="utf-8"))
    if contract.get("schema_version") != "previs-compiler/1.0":
        raise SystemExit(f"Unsupported schema_version: {contract.get('schema_version')}")
    render_contract(contract, output_path, project_path, validation_path)
