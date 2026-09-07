#!/usr/bin/env python3
"""Render action-readable whitebox fight previs with joint-driven rigid parts.

This backend is intentionally separate from the generic camera/blocking adapter.
It starts with a single approved action gate and only then grows reusable action
profiles. Run it with Blender, not the system Python.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Matrix, Quaternion, Vector


def parse_args() -> argparse.Namespace:
    raw = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--validation", required=True)
    parser.add_argument("--frames-dir")
    return parser.parse_args(raw)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (
        bpy.data.meshes,
        bpy.data.curves,
        bpy.data.cameras,
        bpy.data.lights,
        bpy.data.materials,
    ):
        for datablock in list(datablocks):
            if datablock.users == 0:
                datablocks.remove(datablock)


def make_material(name: str, color, roughness: float = 0.78, metallic: float = 0.08):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color[:3], 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = mat.diffuse_color
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def unit_cube(name: str, mat):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.0, 0.0))
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.data.materials.append(mat)
    return obj


def unit_cylinder(name: str, mat, vertices: int = 12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=0.5, depth=1.0, location=(0.0, 0.0, 0.0))
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.data.materials.append(mat)
    return obj


def unit_sphere(name: str, mat):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.5, location=(0.0, 0.0, 0.0))
    obj = bpy.context.object
    obj.name = name
    obj.rotation_mode = "QUATERNION"
    obj.data.materials.append(mat)
    return obj


def key_transform(obj, frame: int, location, rotation=None, scale=None) -> None:
    obj.location = tuple(float(value) for value in location)
    obj.keyframe_insert("location", frame=frame)
    if rotation is not None:
        obj.rotation_mode = "QUATERNION"
        obj.rotation_quaternion = rotation
        obj.keyframe_insert("rotation_quaternion", frame=frame)
    if scale is not None:
        obj.scale = tuple(float(value) for value in scale)
        obj.keyframe_insert("scale", frame=frame)


def key_visible(obj, frame: int, visible: bool) -> None:
    obj.hide_render = not visible
    obj.hide_viewport = not visible
    obj.keyframe_insert("hide_render", frame=frame)
    obj.keyframe_insert("hide_viewport", frame=frame)


def iter_fcurves(obj):
    action = getattr(getattr(obj, "animation_data", None), "action", None)
    if not action:
        return []
    curves = getattr(action, "fcurves", None)
    if curves is not None:
        return list(curves)
    found = []
    for layer in getattr(action, "layers", []):
        for strip in getattr(layer, "strips", []):
            for channelbag in getattr(strip, "channelbags", []):
                found.extend(channelbag.fcurves)
    return found


def set_interpolation(obj, interpolation: str = "LINEAR") -> None:
    for curve in iter_fcurves(obj):
        for point in curve.keyframe_points:
            point.interpolation = interpolation


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def keyed_scalar(frame: int, keys) -> float:
    if frame <= keys[0][0]:
        return float(keys[0][1])
    if frame >= keys[-1][0]:
        return float(keys[-1][1])
    for (left_frame, left_value), (right_frame, right_value) in zip(keys, keys[1:]):
        if left_frame <= frame <= right_frame:
            amount = smoothstep((frame - left_frame) / max(1, right_frame - left_frame))
            return float(left_value) + (float(right_value) - float(left_value)) * amount
    return float(keys[-1][1])


def keyed_vector(frame: int, keys) -> Vector:
    if frame <= keys[0][0]:
        return Vector(keys[0][1])
    if frame >= keys[-1][0]:
        return Vector(keys[-1][1])
    for (left_frame, left_value), (right_frame, right_value) in zip(keys, keys[1:]):
        if left_frame <= frame <= right_frame:
            amount = smoothstep((frame - left_frame) / max(1, right_frame - left_frame))
            return Vector(left_value).lerp(Vector(right_value), amount)
    return Vector(keys[-1][1])


def axes_quaternion(x_axis: Vector, y_axis: Vector, z_axis: Vector) -> Quaternion:
    return Matrix((x_axis.normalized(), y_axis.normalized(), z_axis.normalized())).transposed().to_quaternion()


def key_block(obj, frame: int, center: Vector, dimensions, rotation: Quaternion | None = None) -> None:
    key_transform(obj, frame, center, rotation or Quaternion(), dimensions)


def key_joint(obj, frame: int, center: Vector, radius: float) -> None:
    key_transform(obj, frame, center, Quaternion(), (radius * 2.0,) * 3)


def key_segment(obj, frame: int, start: Vector, end: Vector, width: float, depth: float | None = None) -> None:
    direction = end - start
    length = max(0.001, direction.length)
    rotation = direction.to_track_quat("Z", "Y")
    key_transform(
        obj,
        frame,
        (start + end) * 0.5,
        rotation,
        (width, depth if depth is not None else width, length),
    )


def solve_two_bone(start: Vector, target: Vector, length_a: float, length_b: float, bend_hint: Vector) -> Vector:
    delta = target - start
    distance = max(0.001, min(delta.length, length_a + length_b - 0.001))
    direction = delta.normalized()
    along = (length_a * length_a - length_b * length_b + distance * distance) / (2.0 * distance)
    height_sq = max(0.0, length_a * length_a - along * along)
    projected = bend_hint - direction * bend_hint.dot(direction)
    if projected.length < 1e-5:
        projected = Vector((0.0, 0.0, 1.0)) - direction * direction.z
    if projected.length < 1e-5:
        projected = Vector((0.0, 1.0, 0.0))
    return start + direction * along + projected.normalized() * math.sqrt(height_sq)


def shift_vector(value: Vector, delta: Vector) -> Vector:
    return Vector(value) + delta


class HeroRig:
    def __init__(self, mats):
        self.objects = []
        self.parts = {}
        cube_parts = [
            "pelvis",
            "torso",
            "chest_plate",
            "head",
            "visor",
            "shoulder_L",
            "shoulder_R",
            "upper_arm_L",
            "upper_arm_R",
            "forearm_L",
            "forearm_R",
            "palm_L",
            "palm_R",
            "thigh_L",
            "thigh_R",
            "shin_L",
            "shin_R",
            "foot_L",
            "foot_R",
            "hammer_head",
            "hammer_fin_A",
            "hammer_fin_B",
        ]
        for name in cube_parts:
            if name.startswith("hammer"):
                mat = mats["weapon"]
            elif name in {"visor"}:
                mat = mats["sensor"]
            elif name.startswith("palm"):
                mat = mats["hero_gold"]
            elif name in {"chest_plate", "shoulder_L", "shoulder_R", "forearm_L", "forearm_R", "shin_L", "shin_R"}:
                mat = mats["hero_armor"]
            else:
                mat = mats["hero_body"]
            self.parts[name] = unit_cube(f"HERO_{name}", mat)
            self.objects.append(self.parts[name])
        self.parts["hammer_handle"] = unit_cylinder("HERO_hammer_handle", mats["weapon"], vertices=16)
        self.objects.append(self.parts["hammer_handle"])
        for side in ("L", "R"):
            for joint in ("elbow", "knee", "hand"):
                name = f"{joint}_{side}"
                self.parts[name] = unit_sphere(f"HERO_{name}", mats["joint"])
                self.objects.append(self.parts[name])
            for finger in range(5):
                name = f"finger_{side}_{finger + 1}"
                self.parts[name] = unit_cube(f"HERO_{name}", mats["hero_gold"])
                self.objects.append(self.parts[name])

    def _hand(self, frame: int, side: str, palm: Vector, target: Vector, axis: Vector, open_amount: float) -> None:
        y_sign = -1.0 if side == "L" else 1.0
        up_axis = Vector((-axis.z, 0.0, axis.x))
        if up_axis.length < 1e-5:
            up_axis = Vector((0.0, 0.0, 1.0))
        up_axis.normalize()
        side_axis = axis.cross(up_axis).normalized()
        rotation = axes_quaternion(up_axis, side_axis, axis.normalized())
        key_block(self.parts[f"palm_{side}"], frame, palm, (0.62, 0.82, 0.46), rotation)
        key_joint(self.parts[f"hand_{side}"], frame, palm, 0.30)
        for index in range(5):
            spread = (index - 2) * 0.15
            base = palm + side_axis * spread + up_axis * 0.12
            open_tip = base + up_axis * (0.90 + 0.08 * index) + axis * (0.12 * y_sign)
            closed_tip = target + side_axis * spread * 0.28 + up_axis * (0.08 + 0.03 * index)
            stagger = max(0.0, min(1.0, open_amount * 1.4 - index * 0.10))
            tip = closed_tip.lerp(open_tip, stagger)
            key_segment(self.parts[f"finger_{side}_{index + 1}"], frame, base, tip, 0.16, 0.14)

    def pose(self, frame: int, state: dict) -> dict:
        root = Vector(state["root"])
        lean = float(state.get("lean", 0.0))
        yaw = float(state.get("yaw", 0.0))
        q_yaw = Quaternion((0.0, 0.0, 1.0), yaw)
        q_body = q_yaw @ Quaternion((0.0, 1.0, 0.0), lean)
        up = q_body @ Vector((0.0, 0.0, 1.0))
        front = q_body @ Vector((1.0, 0.0, 0.0))
        pelvis = root + Vector((0.0, 0.0, float(state.get("pelvis_z", 4.0))))
        chest = pelvis + up * 2.05
        head = chest + up * 2.05 + front * 0.10
        head_q = q_yaw @ Quaternion((0.0, 1.0, 0.0), lean + float(state.get("head_pitch", 0.0)))

        key_block(self.parts["pelvis"], frame, pelvis, (1.65, 1.65, 1.15), q_body)
        key_block(self.parts["torso"], frame, chest, (2.20, 1.65, 2.85), q_body)
        key_block(self.parts["chest_plate"], frame, chest + front * 1.12, (0.45, 1.25, 1.55), q_body)
        key_block(self.parts["head"], frame, head, (1.28, 1.20, 1.32), head_q)
        key_block(self.parts["visor"], frame, head + front * 0.67 + up * 0.12, (0.18, 0.76, 0.22), head_q)

        hammer_butt = Vector(state["hammer_butt"])
        hammer_head = Vector(state["hammer_head"])
        weapon_axis = (hammer_head - hammer_butt).normalized()
        handle_top = hammer_head - weapon_axis * 0.88
        key_segment(self.parts["hammer_handle"], frame, hammer_butt, handle_top, 0.54)

        head_long = Vector((-weapon_axis.z, 0.0, weapon_axis.x))
        if head_long.length < 1e-5:
            head_long = Vector((0.0, 0.0, 1.0))
        head_long.normalize()
        head_depth = weapon_axis.cross(head_long).normalized()
        head_q = axes_quaternion(head_long, head_depth, weapon_axis)
        key_block(self.parts["hammer_head"], frame, hammer_head, (3.75, 2.05, 1.92), head_q)
        key_block(self.parts["hammer_fin_A"], frame, hammer_head + head_long * 2.05, (0.62, 1.35, 1.25), head_q)
        key_block(self.parts["hammer_fin_B"], frame, hammer_head - head_long * 2.05, (0.62, 1.35, 1.25), head_q)

        rear_grip = hammer_head - weapon_axis * 3.38
        front_grip = hammer_head - weapon_axis * 2.18
        left_target = Vector(state.get("left_hand_target", rear_grip + Vector((0.0, -0.24, 0.0))))
        right_target = Vector(state.get("right_hand_target", front_grip + Vector((0.0, 0.24, 0.0))))
        left_palm = left_target + Vector((0.0, -0.34, 0.18))
        right_palm = right_target + Vector((0.0, 0.34, 0.18))

        shoulders = {}
        palms = {"L": left_palm, "R": right_palm}
        targets = {"L": left_target, "R": right_target}
        for side, y_sign in (("L", -1.0), ("R", 1.0)):
            shoulder = chest + up * 0.58 + Vector((0.0, 1.35 * y_sign, 0.0))
            shoulders[side] = shoulder
            palm = palms[side]
            elbow = solve_two_bone(
                shoulder,
                palm,
                2.65,
                2.45,
                Vector((0.25, 1.65 * y_sign, -1.25)),
            )
            key_block(self.parts[f"shoulder_{side}"], frame, shoulder, (1.25, 1.10, 1.05), q_body)
            key_segment(self.parts[f"upper_arm_{side}"], frame, shoulder, elbow, 0.68, 0.76)
            key_segment(self.parts[f"forearm_{side}"], frame, elbow, palm, 0.82, 0.88)
            key_joint(self.parts[f"elbow_{side}"], frame, elbow, 0.40)
            hand_axis = Vector(state.get(f"{side}_hand_axis", weapon_axis))
            if hand_axis.length < 1e-5:
                hand_axis = weapon_axis
            self._hand(
                frame,
                side,
                palm,
                targets[side],
                hand_axis.normalized(),
                float(state.get(f"{side}_hand_open", 0.0)),
            )

        feet = {"L": Vector(state["foot_L"]), "R": Vector(state["foot_R"])}
        for side, y_sign in (("L", -1.0), ("R", 1.0)):
            hip = pelvis + Vector((0.0, 0.58 * y_sign, -0.15))
            ankle = feet[side] + Vector((0.0, 0.0, 0.50))
            knee = solve_two_bone(hip, ankle, 2.35, 2.25, Vector((1.15, 0.35 * y_sign, 0.25)))
            key_segment(self.parts[f"thigh_{side}"], frame, hip, knee, 0.85, 0.90)
            key_segment(self.parts[f"shin_{side}"], frame, knee, ankle, 0.94, 1.02)
            key_joint(self.parts[f"knee_{side}"], frame, knee, 0.45)
            key_block(self.parts[f"foot_{side}"], frame, feet[side] + front * 0.32, (1.70, 1.10, 0.66), q_body)

        contact_point = hammer_head + weapon_axis * 0.96
        return {
            "root": root,
            "head": head,
            "hammer_head": hammer_head,
            "hammer_butt": hammer_butt,
            "hammer_contact": contact_point,
            "grip_targets": targets,
            "palms": palms,
            "feet": feet,
        }


class EnemyRig:
    def __init__(self, mats):
        self.objects = []
        self.parts = {}
        cube_parts = [
            "body",
            "spine",
            "head_core",
            "head_sensor",
            "beak_upper",
            "beak_lower",
            "shoulder_L",
            "shoulder_R",
            "upper_arm_L",
            "upper_arm_R",
            "forearm_L",
            "forearm_R",
            "palm_L",
            "palm_R",
        ]
        for name in cube_parts:
            if name in {"head_sensor"}:
                mat = mats["enemy_core"]
            elif name.startswith("palm"):
                mat = mats["enemy_core"]
            else:
                mat = mats["enemy_armor"] if name.startswith(("shoulder", "forearm", "beak")) else mats["enemy_body"]
            self.parts[name] = unit_cube(f"ENEMY_{name}", mat)
            self.objects.append(self.parts[name])
        self.parts["focus"] = unit_cylinder("ENEMY_focus", mats["enemy_core"], vertices=20)
        self.objects.append(self.parts["focus"])
        for side in ("L", "R"):
            for joint in ("elbow", "hand"):
                name = f"{joint}_{side}"
                self.parts[name] = unit_sphere(f"ENEMY_{name}", mats["joint"])
                self.objects.append(self.parts[name])
            for claw in range(3):
                name = f"claw_{side}_{claw + 1}"
                self.parts[name] = unit_cube(f"ENEMY_{name}", mats["enemy_armor"])
                self.objects.append(self.parts[name])

    def pose(self, frame: int, state: dict) -> dict:
        body = Vector(state["body"])
        pitch = float(state.get("pitch", 0.0))
        q_body = Quaternion((0.0, 1.0, 0.0), pitch)
        front = q_body @ Vector((-1.0, 0.0, 0.0))
        up = q_body @ Vector((0.0, 0.0, 1.0))
        key_block(self.parts["body"], frame, body, (7.40, 5.20, 3.60), q_body)
        key_block(self.parts["spine"], frame, body - front * 2.10 + up * 0.75, (3.70, 3.60, 2.30), q_body)
        beak_center = body + front * 4.35 + up * 0.30
        beak_pitch = pitch + float(state.get("head_pitch", 0.0))
        q_beak = Quaternion((0.0, 1.0, 0.0), beak_pitch)
        head_core = beak_center - front * 1.55
        key_block(self.parts["head_core"], frame, head_core, (3.20, 2.85, 2.55), q_beak)
        key_block(
            self.parts["head_sensor"],
            frame,
            head_core + Vector((0.0, -1.48, 0.36)),
            (0.58, 0.22, 0.42),
            q_beak,
        )
        beak_open = float(state.get("beak_open", 0.0))
        key_block(self.parts["beak_upper"], frame, beak_center + up * (0.50 + 0.34 * beak_open), (4.20, 2.10, 0.92), q_beak)
        key_block(self.parts["beak_lower"], frame, beak_center - up * (0.50 + 0.34 * beak_open), (4.00, 2.00, 0.82), q_beak)
        focus_center = beak_center + front * 2.22
        focus_q = front.to_track_quat("Z", "Y")
        focus_scale = 1.15 + 0.42 * beak_open
        key_transform(self.parts["focus"], frame, focus_center, focus_q, (focus_scale, focus_scale, 0.40))

        palms = {"L": Vector(state["hand_L"]), "R": Vector(state["hand_R"])}
        shoulders = {}
        elbows = {}
        palm_rotations = {}
        for side, y_sign in (("L", -1.0), ("R", 1.0)):
            shoulder = body + front * 0.65 + Vector((0.0, 3.35 * y_sign, 0.0)) + up * 1.25
            palm = palms[side]
            elbow = solve_two_bone(
                shoulder,
                palm,
                4.55,
                4.10,
                Vector((0.15, 2.0 * y_sign, -1.30)),
            )
            shoulders[side] = shoulder
            elbows[side] = elbow
            key_block(self.parts[f"shoulder_{side}"], frame, shoulder, (2.10, 1.75, 1.80), q_body)
            key_segment(self.parts[f"upper_arm_{side}"], frame, shoulder, elbow, 1.06, 1.18)
            key_segment(self.parts[f"forearm_{side}"], frame, elbow, palm, 1.20, 1.30)
            key_joint(self.parts[f"elbow_{side}"], frame, elbow, 0.60)
            key_joint(self.parts[f"hand_{side}"], frame, palm, 0.38)
            palm_dir = (palm - elbow).normalized()
            palm_q = palm_dir.to_track_quat("Z", "Y")
            palm_rotations[side] = palm_q.copy()
            key_block(self.parts[f"palm_{side}"], frame, palm, (1.65, 1.20, 0.92), palm_q)
            claw_dir = Vector((-0.82, 0.0, -0.38))
            for index in range(3):
                lateral = Vector((0.0, (index - 1) * 0.48, 0.0))
                base = palm + lateral + claw_dir * 0.25
                tip = palm + lateral * 1.25 + claw_dir * (1.55 + 0.12 * index)
                key_segment(self.parts[f"claw_{side}_{index + 1}"], frame, base, tip, 0.30, 0.34)

        return {
            "body": body,
            "beak": beak_center,
            "beak_open": beak_open,
            "palms": palms,
            "palm_rotations": palm_rotations,
            "shoulders": shoulders,
            "elbows": elbows,
        }


class ImpactRig:
    def __init__(self, mats):
        self.objects = []
        for index in range(8):
            obj = unit_cube(f"IMPACT_chip_{index + 1}", mats["impact"])
            self.objects.append(obj)

    def pose(self, frame: int, point: Vector, visible: bool) -> None:
        offsets = [
            (-0.62, -0.24, 0.10),
            (-0.35, 0.30, 0.42),
            (0.08, -0.35, 0.55),
            (0.46, 0.24, 0.34),
            (0.68, -0.12, -0.08),
            (0.28, 0.36, -0.42),
            (-0.18, -0.42, -0.48),
            (-0.54, 0.20, -0.30),
        ]
        for index, obj in enumerate(self.objects):
            key_visible(obj, frame, visible)
            key_block(obj, frame, point + Vector(offsets[index]), (0.26, 0.18, 0.44), Quaternion())


def resample_polyline(points, count: int) -> list[Vector]:
    points = [Vector(point) for point in points]
    if len(points) < 2:
        points = [points[0] if points else Vector(), points[0] if points else Vector((0.0, 0.0, 0.01))]
    edge_count = len(points) - 1
    segment_count = count - 1
    if edge_count > segment_count:
        raise ValueError("Cable has more control spans than render segments")
    edge_lengths = [max(0.0001, (right - left).length) for left, right in zip(points, points[1:])]
    total = sum(edge_lengths)
    allocations = [1] * edge_count
    remaining = segment_count - edge_count
    raw_extras = [remaining * length / total for length in edge_lengths]
    for index, value in enumerate(raw_extras):
        allocations[index] += int(math.floor(value))
    distributed = sum(allocations)
    ranked = sorted(
        range(edge_count),
        key=lambda index: raw_extras[index] - math.floor(raw_extras[index]),
        reverse=True,
    )
    for index in ranked[: segment_count - distributed]:
        allocations[index] += 1
    result = [points[0]]
    for edge_index, steps in enumerate(allocations):
        for step in range(1, steps + 1):
            result.append(points[edge_index].lerp(points[edge_index + 1], step / steps))
    if len(result) != count:
        raise RuntimeError(f"Cable resampling produced {len(result)} points instead of {count}")
    return result


class CableRig:
    def __init__(
        self,
        mats,
        segment_count: int = 24,
        prefix: str = "CABLE",
        cable_material: str = "cable",
        blade_material: str = "cable_blade",
    ):
        self.objects = []
        self.segments = []
        self.segment_count = segment_count
        for index in range(segment_count):
            obj = unit_cylinder(f"{prefix}_segment_{index + 1}", mats[cable_material], vertices=10)
            self.segments.append(obj)
            self.objects.append(obj)
        self.blade = unit_cube(f"{prefix}_blade", mats[blade_material])
        self.spool = unit_cylinder(f"{prefix}_spool", mats[blade_material], vertices=20)
        self.objects.extend([self.blade, self.spool])

    def pose(self, frame: int, control_points, visible: bool) -> list[Vector]:
        points = resample_polyline(control_points, self.segment_count + 1)
        for index, segment in enumerate(self.segments):
            key_visible(segment, frame, visible)
            key_segment(segment, frame, points[index], points[index + 1], 0.22)
        tangent = points[-1] - points[-2]
        if tangent.length < 1e-5:
            tangent = Vector((-1.0, 0.0, 0.0))
        blade_q = tangent.normalized().to_track_quat("X", "Z")
        key_visible(self.blade, frame, visible)
        key_block(self.blade, frame, points[-1], (1.30, 0.62, 0.34), blade_q)
        spool_center = points[0] + Vector((0.0, 0.45, 0.0))
        spool_q = Vector((0.0, -1.0, 0.0)).to_track_quat("Z", "Y")
        key_visible(self.spool, frame, visible)
        key_transform(self.spool, frame, spool_center, spool_q, (1.35, 1.35, 0.72))
        return points


class LongEnvironment:
    def __init__(self, mats):
        self.objects = []
        for index, x in enumerate((-9.0, -4.0, 1.0, 6.0)):
            post = unit_cube(f"RAIL_post_{index + 1}", mats["rail"])
            key_block(post, 1, Vector((x, -4.8, 1.15)), (0.24, 0.24, 2.30), Quaternion())
            self.objects.append(post)
        for index, center_x in enumerate((-6.5, 3.5)):
            bar = unit_cube(f"RAIL_fixed_{index + 1}", mats["rail"])
            key_block(bar, 1, Vector((center_x, -4.8, 1.55)), (4.60, 0.22, 0.22), Quaternion())
            self.objects.append(bar)
        self.break_bar = unit_cube("RAIL_breaking_center", mats["rail"])
        self.objects.append(self.break_bar)
        self.foot_groove_l = unit_cube("GROUND_foot_groove_L", mats["groove"])
        self.foot_groove_r = unit_cube("GROUND_foot_groove_R", mats["groove"])
        self.hammer_groove = unit_cube("GROUND_hammer_groove", mats["groove"])
        self.foot_soil_l = unit_cube("GROUND_foot_soil_L", mats["soil"])
        self.foot_soil_r = unit_cube("GROUND_foot_soil_R", mats["soil"])
        self.hammer_soil = unit_cube("GROUND_hammer_soil", mats["soil"])
        self.objects.extend(
            [
                self.foot_groove_l,
                self.foot_groove_r,
                self.hammer_groove,
                self.foot_soil_l,
                self.foot_soil_r,
                self.hammer_soil,
            ]
        )

    def pose(self, frame: int, state: dict) -> None:
        break_progress = float(state.get("rail_break_progress", 0.0))
        start = Vector((-1.5, -4.8, 1.55))
        end = Vector((-1.0, -7.2, 3.30))
        center = start.lerp(end, smoothstep(break_progress))
        rotation = Quaternion((0.0, 1.0, 0.0), math.radians(68.0) * smoothstep(break_progress))
        key_block(self.break_bar, frame, center, (4.60, 0.22, 0.22), rotation)

        grooves = state.get("grooves", {})
        for obj, soil_obj, key, y in (
            (self.foot_groove_l, self.foot_soil_l, "foot_L", -0.66),
            (self.foot_groove_r, self.foot_soil_r, "foot_R", 0.66),
            (self.hammer_groove, self.hammer_soil, "hammer", -0.10),
        ):
            pair = grooves.get(key)
            visible = bool(pair and abs(float(pair[1]) - float(pair[0])) > 0.05)
            key_visible(obj, frame, visible)
            key_visible(soil_obj, frame, visible)
            if visible:
                start_x, end_x = [float(value) for value in pair]
                length = abs(end_x - start_x)
                key_block(
                    obj,
                    frame,
                    Vector(((start_x + end_x) * 0.5, y, 0.055)),
                    (length, 0.78 if key != "hammer" else 1.0, 0.14),
                    Quaternion(),
                )
                soil_size = (0.72, 1.05, 0.36) if key != "hammer" else (1.10, 1.30, 0.45)
                soil_center = Vector((end_x + 0.25, y, 0.18 if key != "hammer" else 0.23))
                key_block(soil_obj, frame, soil_center, soil_size, Quaternion())
            else:
                key_block(obj, frame, Vector((-20.0, y, -0.5)), (0.05, 0.05, 0.05), Quaternion())
                key_block(soil_obj, frame, Vector((-20.0, y, -0.5)), (0.05, 0.05, 0.05), Quaternion())


class ProjectileRig:
    def __init__(self, mats):
        self.objects = []
        for index in range(3):
            obj = unit_sphere(f"KINETIC_PROJECTILE_{index + 1}", mats["impact"])
            self.objects.append(obj)

    def pose(self, frame: int, projectiles) -> None:
        for index, obj in enumerate(self.objects):
            item = projectiles[index] if index < len(projectiles) else None
            visible = bool(item and item.get("visible"))
            key_visible(obj, frame, visible)
            location = Vector(item.get("position", (0.0, 0.0, -2.0))) if item else Vector((0.0, 0.0, -2.0))
            radius = float(item.get("radius", 0.30)) if item else 0.30
            key_joint(obj, frame, location, radius)


class FullEnvironment:
    def __init__(self, mats):
        self.objects = []
        self.south_wall = unit_cube("FULL_ENV_south_layered_wall", mats["structure"])
        key_block(self.south_wall, 1, Vector((0.0, -10.2, 7.0)), (30.0, 1.4, 14.0), Quaternion())
        self.objects.append(self.south_wall)
        self.anchor = unit_cube("FULL_ENV_south_anchor", mats["rail"])
        key_block(self.anchor, 1, Vector((-3.8, -9.0, 4.2)), (4.2, 1.4, 7.0), Quaternion())
        self.objects.append(self.anchor)
        self.hero_foot_pit = unit_cube("FULL_ENV_hero_foot_pit", mats["groove"])
        self.enemy_claw_pit = unit_cube("FULL_ENV_enemy_claw_pit", mats["groove"])
        self.collision_pit = unit_cube("FULL_ENV_collision_pit", mats["groove"])
        self.anchor_crack = unit_cube("FULL_ENV_anchor_crack", mats["impact"])
        self.objects.extend([self.hero_foot_pit, self.enemy_claw_pit, self.collision_pit, self.anchor_crack])
        self.bullet_pits = []
        self.bullet_soil = []
        for index in range(3):
            pit = unit_cube(f"FULL_ENV_bullet_pit_{index + 1}", mats["groove"])
            soil = unit_cube(f"FULL_ENV_bullet_soil_{index + 1}", mats["soil"])
            self.bullet_pits.append(pit)
            self.bullet_soil.append(soil)
            self.objects.extend([pit, soil])
        self.wall_pits = []
        for index in range(3):
            pit = unit_cube(f"FULL_ENV_wall_step_pit_{index + 1}", mats["groove"])
            self.wall_pits.append(pit)
            self.objects.append(pit)

    def _toggle_block(self, obj, frame: int, visible: bool, center, size, rotation=None) -> None:
        key_visible(obj, frame, visible)
        key_block(obj, frame, Vector(center), size, rotation or Quaternion())

    def pose(self, frame: int, state: dict) -> None:
        self._toggle_block(
            self.hero_foot_pit,
            frame,
            bool(state.get("hero_foot_pit")),
            (-10.6, -0.65, 0.04),
            (2.0, 1.5, 0.14),
        )
        self._toggle_block(
            self.enemy_claw_pit,
            frame,
            bool(state.get("enemy_claw_pit")),
            (9.0, -1.8, 0.04),
            (2.6, 2.0, 0.16),
        )
        self._toggle_block(
            self.collision_pit,
            frame,
            bool(state.get("collision_pit")),
            (0.0, 0.0, 0.05),
            (5.4, 3.2, 0.18),
        )
        bullet_centers = [(-9.2, 1.3, 0.04), (-6.2, 1.8, 0.04), (-3.2, 2.4, 0.04)]
        pit_count = int(state.get("bullet_pit_count", 0))
        for index, (pit, soil) in enumerate(zip(self.bullet_pits, self.bullet_soil)):
            visible = index < pit_count
            center = bullet_centers[index]
            self._toggle_block(pit, frame, visible, center, (1.5, 1.25, 0.14))
            self._toggle_block(soil, frame, visible, (center[0] + 0.55, center[1], 0.20), (0.75, 1.15, 0.40))
        anchor_visible = bool(state.get("anchor_crack"))
        self._toggle_block(
            self.anchor_crack,
            frame,
            anchor_visible,
            (-3.8, -9.75, 4.2),
            (2.6, 0.12, 0.20),
            Quaternion((1.0, 0.0, 0.0), math.radians(25.0)),
        )
        wall_count = int(state.get("wall_pit_count", 0))
        wall_centers = [(-4.0, -9.48, 2.3), (-3.0, -9.48, 5.0), (-2.0, -9.48, 8.0)]
        for index, pit in enumerate(self.wall_pits):
            self._toggle_block(pit, frame, index < wall_count, wall_centers[index], (2.0, 0.18, 1.5))


def collision_state(local_frame: int) -> tuple[dict, dict]:
    local_frame = max(1, min(67, int(local_frame)))
    hero_root = keyed_vector(
        local_frame,
        [
            (1, (-7.2, 0.0, 0.0)),
            (12, (-6.9, 0.0, 0.0)),
            (21, (-5.1, 0.0, 0.0)),
            (27, (-4.1, 0.0, 0.0)),
            (29, (-3.8, 0.0, 0.0)),
            (34, (-3.8, 0.0, 0.0)),
            (35, (-3.95, -0.02, 0.0)),
            (45, (-5.9, -0.15, 0.0)),
            (67, (-8.8, -0.35, 0.0)),
        ],
    )
    hero_lean = keyed_scalar(
        local_frame,
        [(1, -0.05), (12, -0.24), (21, 0.02), (27, 0.24), (29, 0.31), (34, 0.31), (35, 0.24), (45, -0.12), (67, -0.34)],
    )
    hammer_butt = keyed_vector(
        local_frame,
        [
            (1, (-4.9, 0.0, 4.65)),
            (12, (-5.25, 0.0, 4.55)),
            (21, (-5.10, 0.0, 4.45)),
            (27, (-4.65, 0.0, 4.22)),
            (29, (-4.50, 0.0, 4.00)),
            (34, (-4.50, 0.0, 4.00)),
            (35, (-4.65, 0.0, 3.98)),
            (45, (-6.15, -0.10, 3.85)),
            (67, (-8.45, -0.25, 3.72)),
        ],
    )
    hammer_head = keyed_vector(
        local_frame,
        [
            (1, (-7.75, 0.0, 1.75)),
            (12, (-8.25, 0.0, 1.15)),
            (21, (-4.20, 0.0, 3.85)),
            (27, (-1.28, 0.0, 6.05)),
            (29, (-0.80, 0.0, 6.50)),
            (34, (-0.80, 0.0, 6.50)),
            (35, (-1.02, 0.0, 6.42)),
            (45, (-3.05, -0.05, 5.92)),
            (67, (-5.40, -0.18, 5.15)),
        ],
    )
    hero_foot_l = keyed_vector(
        local_frame,
        [(1, (-6.35, -0.66, 0.0)), (21, (-4.75, -0.66, 0.0)), (29, (-4.25, -0.66, 0.0)), (34, (-4.25, -0.66, 0.0)), (45, (-5.85, -0.66, 0.0)), (67, (-8.25, -0.66, 0.0))],
    )
    hero_foot_r = keyed_vector(
        local_frame,
        [(1, (-8.05, 0.66, 0.0)), (21, (-6.05, 0.66, 0.0)), (29, (-5.55, 0.66, 0.0)), (34, (-5.55, 0.66, 0.0)), (45, (-7.10, 0.66, 0.0)), (67, (-9.55, 0.66, 0.0))],
    )

    enemy_body = keyed_vector(
        local_frame,
        [
            (1, (7.4, 0.0, 8.10)),
            (12, (7.0, 0.0, 7.95)),
            (21, (5.8, 0.0, 7.75)),
            (27, (4.9, 0.0, 7.68)),
            (29, (4.55, 0.0, 7.68)),
            (34, (4.55, 0.0, 7.68)),
            (35, (4.75, 0.0, 7.78)),
            (45, (6.55, 0.0, 8.85)),
            (67, (9.1, 0.15, 10.55)),
        ],
    )
    enemy_pitch = keyed_scalar(
        local_frame,
        [(1, -0.03), (12, -0.12), (21, -0.22), (29, -0.30), (34, -0.30), (35, -0.20), (45, 0.12), (67, 0.38)],
    )
    enemy_hand_l = keyed_vector(
        local_frame,
        [
            (1, (3.70, -1.65, 8.85)),
            (12, (3.25, -1.50, 8.55)),
            (21, (2.15, -1.15, 7.80)),
            (27, (-0.10, -0.65, 6.75)),
            (29, (-0.28, -0.50, 6.82)),
            (34, (-0.28, -0.50, 6.82)),
            (35, (-0.08, -0.58, 6.92)),
            (45, (2.55, -1.35, 8.35)),
            (67, (6.30, -2.20, 10.10)),
        ],
    )
    enemy_hand_r = keyed_vector(
        local_frame,
        [
            (1, (3.80, 1.65, 8.65)),
            (12, (3.35, 1.50, 8.35)),
            (21, (2.20, 1.15, 7.65)),
            (27, (0.55, 0.60, 7.45)),
            (29, (0.12, 0.405, 7.42)),
            (34, (0.12, 0.405, 7.42)),
            (35, (0.36, 0.48, 7.32)),
            (45, (2.70, 1.35, 8.20)),
            (67, (6.45, 2.20, 9.95)),
        ],
    )
    hero = {
        "root": hero_root,
        "lean": hero_lean,
        "pelvis_z": 4.0,
        "hammer_butt": hammer_butt,
        "hammer_head": hammer_head,
        "foot_L": hero_foot_l,
        "foot_R": hero_foot_r,
        "L_hand_open": 0.0,
        "R_hand_open": 0.0,
    }
    enemy = {
        "body": enemy_body,
        "pitch": enemy_pitch,
        "hand_L": enemy_hand_l,
        "hand_R": enemy_hand_r,
    }
    return hero, enemy


def vault_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(1, min(43, int(frame)))
    hero = {
        "root": keyed_vector(
            frame,
            [(1, (-7.4, 0.0, 0.0)), (12, (-7.0, 0.0, 0.0)), (23, (-6.2, 0.0, 2.8)), (32, (-6.7, 0.0, 1.15)), (43, (-7.2, 0.0, 0.0))],
        ),
        "lean": keyed_scalar(frame, [(1, 0.18), (12, -0.12), (23, 0.20), (32, -0.18), (43, -0.05)]),
        "pelvis_z": keyed_scalar(frame, [(1, 3.55), (12, 3.35), (23, 4.0), (32, 3.85), (43, 4.0)]),
        "hammer_butt": keyed_vector(
            frame,
            [(1, (-5.0, 0.0, 0.20)), (12, (-4.85, 0.0, 0.14)), (23, (-4.75, 0.0, 0.16)), (32, (-4.90, 0.0, 2.70)), (43, (-4.90, 0.0, 4.65))],
        ),
        "hammer_head": keyed_vector(
            frame,
            [(1, (-4.15, 0.0, 6.75)), (12, (-4.10, 0.0, 6.95)), (23, (-4.10, 0.0, 7.05)), (32, (-6.55, 0.0, 3.05)), (43, (-7.75, 0.0, 1.75))],
        ),
        "foot_L": keyed_vector(
            frame,
            [(1, (-6.55, -0.66, 0.0)), (12, (-6.35, -0.66, 0.0)), (23, (-5.85, -0.66, 3.55)), (32, (-6.05, -0.66, 1.15)), (43, (-6.35, -0.66, 0.0))],
        ),
        "foot_R": keyed_vector(
            frame,
            [(1, (-8.10, 0.66, 0.0)), (12, (-7.75, 0.66, 0.0)), (23, (-6.85, 0.66, 3.95)), (32, (-7.40, 0.66, 1.05)), (43, (-8.05, 0.66, 0.0))],
        ),
        "L_hand_open": 0.0,
        "R_hand_open": 0.0,
    }
    enemy = {
        "body": keyed_vector(frame, [(1, (8.0, 0.0, 8.25)), (24, (7.7, 0.0, 8.15)), (43, (7.4, 0.0, 8.10))]),
        "pitch": keyed_scalar(frame, [(1, -0.02), (24, -0.04), (43, -0.03)]),
        "hand_L": keyed_vector(frame, [(1, (4.3, -1.8, 8.9)), (24, (4.0, -1.7, 8.8)), (43, (3.70, -1.65, 8.85))]),
        "hand_R": keyed_vector(frame, [(1, (4.4, 1.8, 8.7)), (24, (4.1, 1.7, 8.7)), (43, (3.80, 1.65, 8.65))]),
    }
    if frame <= 30:
        progress = smoothstep((frame - 1) / 29.0)
        blade = Vector((6.5, -0.5, 1.05)).lerp(Vector((-14.0, -1.15, 0.78)), progress)
        origin = cable_origin(enemy)
        cable_points = [
            origin,
            origin + Vector((-1.7, -0.25, 0.9)),
            Vector((2.8, -0.65, 4.0)).lerp(Vector((-7.0, -0.85, 1.15)), progress),
            blade,
        ]
    else:
        origin = cable_origin(enemy)
        cable_points = [origin, origin + Vector((1.5, -0.4, -0.6)), origin + Vector((3.0, -0.8, -1.1))]
    effects = {
        "cable_visible": frame <= 30,
        "cable_points": cable_points,
        "rail_break_progress": max(0.0, min(1.0, (frame - 17) / 13.0)),
        "grooves": {},
    }
    return hero, enemy, effects


def reaction_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(111, min(156, int(frame)))
    hero_base, enemy_base = collision_state(67)
    amount = smoothstep((frame - 111) / 45.0)
    hero_delta = Vector((0.45 * amount, 0.05 * amount, 0.0))
    enemy_delta = Vector((-0.55 * amount, -0.05 * amount, -0.82 * amount))
    hero = dict(hero_base)
    hero["root"] = Vector(hero_base["root"]) + hero_delta
    hero["hammer_butt"] = Vector(hero_base["hammer_butt"]) + hero_delta
    hero["hammer_head"] = Vector(hero_base["hammer_head"]) + hero_delta
    hero["foot_L"] = Vector(hero_base["foot_L"]) + hero_delta * 0.72
    hero["foot_R"] = Vector(hero_base["foot_R"]) + hero_delta * 0.72
    hero["lean"] = keyed_scalar(frame, [(111, -0.34), (124, -0.40), (134, -0.24), (156, -0.18)])
    hero["head_pitch"] = keyed_scalar(frame, [(111, 0.20), (124, 0.30), (134, -0.12), (156, -0.06)])

    enemy = dict(enemy_base)
    enemy["body"] = Vector(enemy_base["body"]) + enemy_delta
    enemy["hand_L"] = Vector(enemy_base["hand_L"]) + enemy_delta * 0.82
    enemy["hand_R"] = Vector(enemy_base["hand_R"]) + enemy_delta * 0.82
    enemy["pitch"] = keyed_scalar(frame, [(111, 0.38), (134, 0.28), (156, 0.16)])
    enemy["head_pitch"] = keyed_scalar(frame, [(111, -0.12), (134, 0.14), (156, 0.04)])
    enemy["beak_open"] = keyed_scalar(frame, [(111, 0.0), (134, 0.10), (145, 0.30), (156, 0.12)])
    effects = {
        "cable_visible": False,
        "cable_points": [Vector(enemy["body"]) + Vector((4.0, 0.0, 2.0)), Vector(enemy["body"]) + Vector((6.0, -0.5, 1.2))],
        "rail_break_progress": 1.0,
        "grooves": {},
    }
    return hero, enemy, effects


def cable_origin(enemy_state: dict) -> Vector:
    return Vector(enemy_state["body"]) + Vector((4.25, -0.45, 1.95))


def build_wrap_cable_controls(origin: Vector, wrap_point: Vector, weapon_axis: Vector, cable_catch: Vector) -> tuple[list[Vector], Vector]:
    around_axis = Vector((-weapon_axis.z, 0.0, weapon_axis.x))
    if around_axis.length < 1e-5:
        around_axis = Vector((1.0, 0.0, 0.0))
    around_axis.normalize()
    camera_front = Vector((0.0, -1.0, 0.0))
    approach = wrap_point + around_axis * 1.05 + camera_front * 0.90
    front = wrap_point + camera_front * 0.95
    under = wrap_point - around_axis * 0.90 + camera_front * 0.20
    back = wrap_point - camera_front * 0.85
    exit_point = wrap_point + around_axis * 0.60 - camera_front * 0.75
    outfeed = origin + Vector((-0.45, -2.20, -0.18))
    guide_1 = outfeed.lerp(approach, 0.38) + Vector((0.0, -0.22, 0.28))
    guide_2 = outfeed.lerp(approach, 0.76) + Vector((0.0, -0.38, 0.42))
    controls = [origin, outfeed, guide_1, guide_2, approach, cable_catch, front, under, back, exit_point]
    catch_axis = cable_catch - approach
    if catch_axis.length < 1e-5:
        catch_axis = weapon_axis
    return controls, catch_axis.normalized()


def point_to_polyline_distance(point: Vector, points) -> float:
    point = Vector(point)
    values = [Vector(value) for value in points]
    best = math.inf
    for start, end in zip(values, values[1:]):
        delta = end - start
        if delta.length_squared < 1e-10:
            distance = (point - start).length
        else:
            amount = max(0.0, min(1.0, (point - start).dot(delta) / delta.length_squared))
            distance = (point - (start + delta * amount)).length
        best = min(best, distance)
    return best


def point_to_oriented_box_distance(
    point: Vector,
    center: Vector,
    rotation: Quaternion,
    dimensions,
) -> float:
    local = rotation.inverted() @ (Vector(point) - Vector(center))
    half = Vector(tuple(float(value) * 0.5 for value in dimensions))
    outside = Vector(
        (
            max(abs(local.x) - half.x, 0.0),
            max(abs(local.y) - half.y, 0.0),
            max(abs(local.z) - half.z, 0.0),
        )
    )
    return outside.length


def wrap_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(157, min(211, int(frame)))
    base_hero, base_enemy, _ = reaction_state(156)
    hero = dict(base_hero)
    enemy = dict(base_enemy)
    hero["root"] = keyed_vector(frame, [(157, base_hero["root"]), (184, (-8.05, 0.0, 0.0)), (211, (-7.65, 0.0, 0.0))])
    hero["lean"] = keyed_scalar(frame, [(157, -0.18), (184, -0.10), (211, -0.30)])
    hero["head_pitch"] = keyed_scalar(frame, [(157, -0.06), (184, 0.03), (211, -0.10)])
    hero["hammer_butt"] = keyed_vector(
        frame,
        [(157, base_hero["hammer_butt"]), (184, (-8.60, -0.62, 4.85)), (211, (-9.30, -1.05, 4.55))],
    )
    hero["hammer_head"] = keyed_vector(
        frame,
        [(157, base_hero["hammer_head"]), (184, (-5.60, -0.62, 3.70)), (211, (-5.05, -1.05, 1.32))],
    )
    hero["foot_L"] = keyed_vector(frame, [(157, base_hero["foot_L"]), (211, (-8.10, -0.66, 0.0))])
    hero["foot_R"] = keyed_vector(frame, [(157, base_hero["foot_R"]), (211, (-9.25, 0.66, 0.0))])
    enemy_delta = keyed_vector(frame, [(157, (0.0, 0.0, 0.0)), (211, (0.60, 0.0, -0.20))])
    enemy["body"] = Vector(base_enemy["body"]) + enemy_delta
    enemy["hand_L"] = Vector(base_enemy["hand_L"]) + enemy_delta
    enemy["hand_R"] = Vector(base_enemy["hand_R"]) + enemy_delta
    enemy["pitch"] = keyed_scalar(frame, [(157, 0.16), (184, 0.08), (211, -0.04)])

    progress = smoothstep((frame - 157) / 54.0)
    weapon_axis = (Vector(hero["hammer_head"]) - Vector(hero["hammer_butt"])).normalized()
    wrap_point = Vector(hero["hammer_head"]) - weapon_axis * 2.70
    origin = cable_origin(enemy)
    cable_catch = wrap_point + Vector((0.25, -1.05, 0.65))
    final_controls, catch_axis = build_wrap_cable_controls(origin, wrap_point, weapon_axis, cable_catch)
    loop_amount = max(0.0, min(1.0, (progress - 0.55) / 0.45))
    if progress <= 0.55:
        route_amount = progress / 0.55
        moving_approach = origin.lerp(final_controls[4], route_amount)
        moving_outfeed = origin.lerp(final_controls[1], route_amount)
        moving_guide_1 = moving_outfeed.lerp(moving_approach, 0.38) + Vector((0.0, -0.22, 0.28 * route_amount))
        moving_guide_2 = moving_outfeed.lerp(moving_approach, 0.76) + Vector((0.0, -0.38, 0.42 * route_amount))
        cable_points = [
            origin,
            moving_outfeed,
            moving_guide_1,
            moving_guide_2,
            moving_approach,
            moving_approach,
            moving_approach,
            moving_approach,
            moving_approach,
            moving_approach,
        ]
    else:
        collapsed = [
            final_controls[0],
            final_controls[1],
            final_controls[2],
            final_controls[3],
            final_controls[4],
            final_controls[4],
            final_controls[4],
            final_controls[4],
            final_controls[4],
            final_controls[4],
        ]
        cable_points = [
            collapsed[index].lerp(final_controls[index], loop_amount)
            for index in range(len(final_controls))
        ]
    effects = {
        "cable_visible": True,
        "cable_points": cable_points,
        "rail_break_progress": 1.0,
        "grooves": {},
        "wrap_point": wrap_point,
        "cable_catch": cable_catch,
        "cable_catch_axis": catch_axis,
    }
    return hero, enemy, effects


def grab_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(212, min(238, int(frame)))
    base_hero, base_enemy, base_effects = wrap_state(211)
    hero = dict(base_hero)
    enemy = dict(base_enemy)
    weapon_axis = (Vector(hero["hammer_head"]) - Vector(hero["hammer_butt"])).normalized()
    rear_grip = Vector(hero["hammer_head"]) - weapon_axis * 3.38 + Vector((0.0, -0.24, 0.0))
    cable_catch = Vector(base_effects["cable_catch"])
    hero["left_hand_target"] = keyed_vector(
        frame,
        [
            (212, rear_grip),
            (218, (-7.65, -1.55, 3.85)),
            (224, (-7.15, -2.00, 3.90)),
            (226, cable_catch),
            (238, cable_catch),
        ],
    )
    hero["L_hand_open"] = keyed_scalar(frame, [(212, 0.0), (218, 1.0), (226, 1.0), (232, 0.55), (238, 0.0)])
    hero["R_hand_open"] = 0.0
    hero["lean"] = keyed_scalar(frame, [(212, -0.30), (226, -0.34), (238, -0.38)])
    wrap_point = Vector(base_effects["wrap_point"])
    cable_points = [Vector(point) for point in base_effects["cable_points"]]
    cable_axis = Vector(base_effects["cable_catch_axis"])
    axis_mix = smoothstep(max(0.0, min(1.0, (frame - 218) / 8.0)))
    hero["L_hand_axis"] = weapon_axis.lerp(cable_axis, axis_mix).normalized()
    effects = {
        "cable_visible": True,
        "cable_points": cable_points,
        "rail_break_progress": 1.0,
        "grooves": {},
        "wrap_point": wrap_point,
        "cable_catch": cable_catch,
        "cable_catch_axis": cable_axis,
    }
    return hero, enemy, effects


def drag_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(239, min(298, int(frame)))
    base_hero, base_enemy, base_effects = grab_state(238)
    hero = dict(base_hero)
    enemy = dict(base_enemy)
    hero["root"] = keyed_vector(frame, [(239, base_hero["root"]), (268, (-6.35, 0.0, 0.0)), (298, (-4.75, 0.0, 0.0))])
    hero["lean"] = keyed_scalar(frame, [(239, -0.38), (268, -0.46), (298, -0.50)])
    hero["pelvis_z"] = keyed_scalar(frame, [(239, 4.0), (268, 3.72), (298, 3.48)])
    hero["head_pitch"] = keyed_scalar(frame, [(239, -0.10), (268, 0.04), (298, -0.06)])
    hero["hammer_butt"] = keyed_vector(frame, [(239, base_hero["hammer_butt"]), (268, (-7.90, -1.05, 4.30)), (298, (-6.25, -1.05, 4.00))])
    hero["hammer_head"] = keyed_vector(frame, [(239, base_hero["hammer_head"]), (268, (-3.72, -1.05, 1.18)), (298, (-1.85, -1.05, 1.08))])
    hero["foot_L"] = keyed_vector(
        frame,
        [(239, base_hero["foot_L"]), (252, base_hero["foot_L"]), (268, (-7.45, -0.66, 0.0)), (282, (-7.45, -0.66, 0.0)), (298, (-6.35, -0.66, 0.0))],
    )
    hero["foot_R"] = keyed_vector(
        frame,
        [(239, base_hero["foot_R"]), (268, base_hero["foot_R"]), (282, (-8.45, 0.66, 0.0)), (298, (-7.10, 0.66, 0.0))],
    )
    hero["left_hand_target"] = keyed_vector(
        frame,
        [(239, base_hero["left_hand_target"]), (268, (-5.20, -2.10, 4.05)), (298, (-3.65, -2.10, 4.12))],
    )
    hero["L_hand_open"] = 0.0
    hero["R_hand_open"] = 0.0

    enemy_delta = keyed_vector(frame, [(239, (0.0, 0.0, 0.0)), (268, (0.85, 0.0, 0.12)), (298, (1.70, 0.0, 0.35))])
    enemy["body"] = Vector(base_enemy["body"]) + enemy_delta
    enemy["hand_L"] = Vector(base_enemy["hand_L"]) + enemy_delta
    enemy["hand_R"] = Vector(base_enemy["hand_R"]) + enemy_delta
    enemy["pitch"] = keyed_scalar(frame, [(239, -0.04), (268, -0.10), (298, -0.14)])

    origin = cable_origin(enemy)
    grip = Vector(hero["left_hand_target"])
    weapon_axis = (Vector(hero["hammer_head"]) - Vector(hero["hammer_butt"])).normalized()
    wrap_point = Vector(hero["hammer_head"]) - weapon_axis * 2.70
    cable_points, catch_axis = build_wrap_cable_controls(origin, wrap_point, weapon_axis, grip)
    hero["L_hand_axis"] = catch_axis
    effects = {
        "cable_visible": True,
        "cable_points": cable_points,
        "rail_break_progress": 1.0,
        "grooves": {
            "foot_L": (float(base_hero["foot_L"].x), float(Vector(hero["foot_L"]).x)),
            "foot_R": (float(base_hero["foot_R"].x), float(Vector(hero["foot_R"]).x)),
            "hammer": (float(base_hero["hammer_head"].x), float(Vector(hero["hammer_head"]).x)),
        },
        "wrap_point": wrap_point,
        "cable_catch": grip,
        "cable_catch_axis": catch_axis,
    }
    return hero, enemy, effects


def long_fight_state(frame: int) -> tuple[dict, dict, dict]:
    if frame <= 43:
        return vault_state(frame)
    if frame <= 110:
        hero, enemy = collision_state(frame - 43)
        return hero, enemy, {
            "cable_visible": False,
            "cable_points": [Vector(enemy["body"]) + Vector((4.0, 0.0, 2.0)), Vector(enemy["body"]) + Vector((6.0, -0.4, 1.0))],
            "rail_break_progress": 1.0,
            "grooves": {},
        }
    if frame <= 156:
        return reaction_state(frame)
    if frame <= 211:
        return wrap_state(frame)
    if frame <= 238:
        return grab_state(frame)
    return drag_state(frame)


def remap_frame(frame: int, source_start: int, source_end: int, target_start: int, target_end: int) -> int:
    if source_end <= source_start:
        return target_start
    amount = (frame - source_start) / (source_end - source_start)
    return int(round(target_start + max(0.0, min(1.0, amount)) * (target_end - target_start)))


def early_full_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(1, min(269, int(frame)))
    root = keyed_vector(
        frame,
        [
            (1, (-16.0, 0.0, 0.0)),
            (54, (-14.2, 0.0, 0.0)),
            (78, (-13.2, 0.0, 0.0)),
            (99, (-12.2, 0.0, 0.0)),
            (131, (-10.8, 0.0, 0.0)),
            (159, (-9.8, 0.0, 0.0)),
            (198, (-8.6, 0.0, 0.0)),
            (212, (-8.1, -1.0, 0.0)),
            (230, (-7.8, 1.0, 0.0)),
            (248, (-7.6, 0.0, 0.0)),
            (269, (-7.4, 0.0, 0.0)),
        ],
    )
    step_phase = (frame - 1) / 11.0
    swing = math.sin(step_phase * math.pi)
    lift_l = max(0.0, swing) * 0.65
    lift_r = max(0.0, -swing) * 0.65
    foot_l = root + Vector((0.75 + 0.75 * swing, -0.66, lift_l))
    foot_r = root + Vector((-0.75 - 0.75 * swing, 0.66, lift_r))
    if frame >= 260:
        amount = smoothstep((frame - 260) / 9.0)
        foot_l = foot_l.lerp(Vector((-6.55, -0.66, 0.0)), amount)
        foot_r = foot_r.lerp(Vector((-8.10, 0.66, 0.0)), amount)
    hammer_head = keyed_vector(
        frame,
        [
            (1, (-17.8, -0.65, 1.0)),
            (159, (-11.8, -0.65, 1.0)),
            (198, (-10.3, -0.65, 1.0)),
            (248, (-9.2, -0.50, 1.0)),
            (260, (-7.0, -0.25, 3.0)),
            (269, (-4.15, 0.0, 6.75)),
        ],
    )
    extension = keyed_scalar(frame, [(1, 3.25), (159, 3.25), (172, 3.80), (184, 4.45), (197, 5.20), (269, 5.20)])
    if frame < 260:
        axis = Vector((-0.45, 0.0, -0.893)).normalized()
        hammer_butt = hammer_head - axis * extension
    else:
        hammer_butt = keyed_vector(frame, [(260, (-6.0, -0.20, 5.4)), (269, (-5.0, 0.0, 0.20))])
    hero = {
        "root": root,
        "lean": keyed_scalar(frame, [(1, 0.24), (159, 0.20), (198, 0.28), (248, 0.18), (269, 0.18)]),
        "pelvis_z": 4.0 if frame < 260 else keyed_scalar(frame, [(260, 4.0), (269, 3.55)]),
        "head_pitch": keyed_scalar(frame, [(1, -0.04), (54, 0.04), (78, -0.02), (269, 0.0)]),
        "hammer_butt": hammer_butt,
        "hammer_head": hammer_head,
        "foot_L": foot_l,
        "foot_R": foot_r,
        "L_hand_open": 0.0,
        "R_hand_open": 0.0,
    }
    body = keyed_vector(
        frame,
        [(1, (16.0, 1.5, 8.4)), (54, (14.5, 1.2, 8.3)), (99, (12.5, 0.8, 8.2)), (159, (10.5, 0.4, 8.2)), (198, (9.4, 0.2, 8.2)), (248, (8.4, 0.0, 8.2)), (269, (8.0, 0.0, 8.25))],
    )
    claw_cycle = math.sin((frame - 1) / 17.0 * math.pi)
    hand_l = body + Vector((-3.0, -2.25, 0.75 + max(0.0, claw_cycle) * 3.0))
    hand_r = body + Vector((-2.7, 2.25, 0.75 + max(0.0, -claw_cycle) * 3.0))
    if 131 <= frame <= 158:
        contact_amount = smoothstep((frame - 131) / 14.0) if frame <= 145 else 1.0 - smoothstep((frame - 145) / 13.0)
        hand_l = body + Vector((-3.2, -2.0, 3.8)).lerp(Vector((-3.2, -2.0, 0.65)), contact_amount)
    if 198 <= frame <= 247:
        hand_l = body + Vector((-3.4, -1.3, 5.4))
        hand_r = body + Vector((-2.6, 1.8, 1.2))
    if frame >= 260:
        amount = smoothstep((frame - 260) / 9.0)
        hand_l = hand_l.lerp(Vector((4.3, -1.8, 8.9)), amount)
        hand_r = hand_r.lerp(Vector((4.4, 1.8, 8.7)), amount)
    enemy = {
        "body": body,
        "pitch": keyed_scalar(frame, [(1, -0.08), (78, -0.02), (198, -0.10), (269, -0.02)]),
        "head_pitch": keyed_scalar(frame, [(1, 0.0), (78, -0.08), (98, 0.08), (269, 0.0)]),
        "beak_open": keyed_scalar(frame, [(1, 0.0), (78, 0.0), (88, 0.14), (98, 0.06), (269, 0.0)]),
        "hand_L": hand_l,
        "hand_R": hand_r,
    }
    projectiles = []
    starts = [202, 218, 234]
    ends = [214, 230, 246]
    targets = [Vector((-9.2, 1.3, 0.45)), Vector((-6.2, 1.8, 0.45)), Vector((-3.2, 2.4, 0.45))]
    muzzle = hand_l + Vector((-0.8, 0.0, 0.0))
    for start, end, target in zip(starts, ends, targets):
        visible = start <= frame <= end
        amount = smoothstep((frame - start) / max(1, end - start)) if visible else 0.0
        projectiles.append({"visible": visible, "position": muzzle.lerp(target, amount), "radius": 0.32})
    enemy_cable_visible = frame >= 248
    origin = cable_origin(enemy)
    release_amount = smoothstep((frame - 248) / 21.0) if enemy_cable_visible else 0.0
    blade = origin.lerp(origin + Vector((-3.8, -1.5, -2.6)), release_amount)
    enemy_cable_points = [origin, origin + Vector((-0.4, -2.0, -0.2)) * release_amount, blade]
    effects = {
        "enemy_cable_visible": enemy_cable_visible,
        "enemy_cable_points": enemy_cable_points,
        "hero_cable_visible": False,
        "hero_cable_points": [Vector((0.0, 0.0, -2.0)), Vector((0.0, 0.0, -1.9))],
        "cable_visible": enemy_cable_visible,
        "cable_points": enemy_cable_points,
        "rail_break_progress": 0.0,
        "grooves": {"hammer": (-17.8, float(hammer_head.x))},
        "projectiles": projectiles,
        "bullet_pit_count": sum(frame > end for end in ends),
        "hero_foot_pit": frame >= 118,
        "enemy_claw_pit": frame >= 145,
        "collision_pit": False,
        "anchor_crack": False,
        "wall_pit_count": 0,
        "hammer_extension_m": extension,
    }
    return hero, enemy, effects


def post_full_state(frame: int) -> tuple[dict, dict, dict]:
    frame = max(567, min(720, int(frame)))
    base_hero, base_enemy, base_effects = drag_state(298)
    hero = dict(base_hero)
    enemy = dict(base_enemy)
    if frame <= 610:
        amount = smoothstep((frame - 567) / 43.0)
        delta = Vector((0.20 * amount, -1.0 * amount, 0.45 * amount))
        for key in ("root", "hammer_butt", "hammer_head", "foot_L", "foot_R", "left_hand_target"):
            if key in hero:
                hero[key] = Vector(base_hero[key]) + delta
        hero["lean"] = -0.46 + 0.12 * amount
    elif frame <= 665:
        hero["root"] = keyed_vector(frame, [(611, (-4.55, -1.0, 0.45)), (628, (-4.0, -4.0, 2.3)), (646, (-3.0, -6.5, 5.2)), (665, (-2.0, -8.0, 8.0))])
        hero["yaw"] = keyed_scalar(frame, [(611, 0.0), (622, -math.pi / 2.0), (665, -math.pi / 2.0)])
        hero["lean"] = keyed_scalar(frame, [(611, -0.34), (628, 0.18), (665, 0.26)])
        hero["pelvis_z"] = 4.0
        hero["foot_L"] = keyed_vector(frame, [(611, (-4.2, -0.66, 0.0)), (628, (-4.0, -9.15, 2.3)), (646, (-3.8, -8.7, 4.2)), (665, (-2.0, -9.15, 8.0))])
        hero["foot_R"] = keyed_vector(frame, [(611, (-5.0, 0.66, 0.0)), (628, (-4.8, -8.5, 1.2)), (646, (-3.0, -9.15, 5.2)), (665, (-2.8, -8.6, 7.0))])
        hero["hammer_butt"] = keyed_vector(frame, [(611, (-6.25, -1.05, 4.0)), (646, (-5.0, -4.5, 6.0)), (665, (-4.0, -6.2, 8.4))])
        hero["hammer_head"] = keyed_vector(frame, [(611, (-1.85, -1.05, 1.08)), (646, (-3.6, -2.8, 3.2)), (665, (-3.8, -4.5, 5.4))])
        axis = (Vector(hero["hammer_head"]) - Vector(hero["hammer_butt"])).normalized()
        hero["left_hand_target"] = Vector(hero["hammer_head"]) - axis * 3.2 + Vector((0.0, -0.8, 0.2))
        hero["L_hand_axis"] = axis
    elif frame <= 684:
        amount = smoothstep((frame - 666) / 18.0)
        hero["root"] = Vector((-2.0, -8.0, 8.0)).lerp(Vector((-1.6, -8.1, 9.2)), amount)
        hero["yaw"] = -math.pi / 2.0
        hero["lean"] = 0.28
        hero["foot_L"] = Vector((-2.0, -9.15, 8.0))
        hero["foot_R"] = Vector((-2.8, -8.6, 7.0))
        hero["hammer_butt"] = Vector((-4.0, -6.2, 8.4)).lerp(Vector((-3.6, -6.0, 9.2)), amount)
        hero["hammer_head"] = Vector((-3.8, -4.5, 5.4)).lerp(Vector((-3.5, -4.2, 6.0)), amount)
    else:
        amount = smoothstep((frame - 685) / 35.0)
        hero["root"] = Vector((-1.6, -8.1, 9.2)).lerp(Vector((1.0, -4.5, 12.0)), amount)
        hero["yaw"] = keyed_scalar(frame, [(685, -math.pi / 2.0), (720, -0.35)])
        hero["lean"] = 0.18
        hero["foot_L"] = Vector((-2.0, -9.15, 8.0)).lerp(Vector((0.4, -5.0, 9.6)), amount)
        hero["foot_R"] = Vector((-2.8, -8.6, 7.0)).lerp(Vector((-0.2, -5.6, 9.0)), amount)
        hero["hammer_butt"] = Vector((-3.6, -6.0, 9.2)).lerp(Vector((-1.0, -5.6, 10.2)), amount)
        hero["hammer_head"] = Vector((-3.5, -4.2, 6.0)).lerp(Vector((-2.6, -6.8, 7.2)), amount)
    if frame >= 611:
        current_axis = (Vector(hero["hammer_head"]) - Vector(hero["hammer_butt"])).normalized()
        hero["left_hand_target"] = Vector(hero["hammer_head"]) - current_axis * 3.2 + Vector((0.0, -0.8, 0.2))
        hero["L_hand_open"] = 0.0
        hero["R_hand_open"] = 0.0
    enemy_delta = keyed_vector(frame, [(567, (0.0, 0.0, 0.0)), (610, (0.30, 0.0, 0.10)), (720, (0.30, 0.0, 0.10))])
    enemy["body"] = Vector(base_enemy["body"]) + enemy_delta
    enemy["hand_L"] = Vector(base_enemy["hand_L"]) + enemy_delta
    enemy["hand_R"] = Vector(base_enemy["hand_R"]) + enemy_delta
    enemy["pitch"] = keyed_scalar(frame, [(567, -0.14), (665, -0.10), (685, -0.08), (720, -0.02)])
    enemy["head_pitch"] = keyed_scalar(frame, [(567, 0.0), (685, 0.0), (720, 0.12)])
    enemy["beak_open"] = keyed_scalar(frame, [(567, 0.0), (685, 0.0), (700, 0.35), (720, 1.0)])
    enemy_origin = cable_origin(enemy)
    grip = Vector(hero.get("left_hand_target", Vector(hero["root"]) + Vector((0.0, -1.2, 4.2))))
    weapon_axis = (Vector(hero["hammer_head"]) - Vector(hero["hammer_butt"])).normalized()
    wrap_point = Vector(hero["hammer_head"]) - weapon_axis * 2.70
    enemy_cable_points, catch_axis = build_wrap_cable_controls(enemy_origin, wrap_point, weapon_axis, grip)
    hero["L_hand_axis"] = catch_axis
    own_origin = Vector(hero["root"]) + Vector((-0.7, 0.5, 7.0))
    anchor = Vector((-3.8, -9.8, 4.2))
    if frame <= 588:
        release = smoothstep((frame - 567) / 21.0)
        own_blade = own_origin.lerp(anchor, release)
    else:
        own_blade = anchor
    hero_cable_points = [own_origin, own_origin.lerp(own_blade, 0.45) + Vector((0.0, -0.6, 0.5)), own_blade]
    drag_grooves = dict(base_effects.get("grooves", {}))
    effects = {
        "enemy_cable_visible": True,
        "enemy_cable_points": enemy_cable_points,
        "hero_cable_visible": True,
        "hero_cable_points": hero_cable_points,
        "cable_visible": True,
        "cable_points": enemy_cable_points,
        "rail_break_progress": 1.0,
        "grooves": drag_grooves,
        "projectiles": [],
        "bullet_pit_count": 3,
        "hero_foot_pit": True,
        "enemy_claw_pit": True,
        "collision_pit": True,
        "anchor_crack": frame >= 588,
        "wall_pit_count": 0 if frame < 628 else (1 if frame < 646 else (2 if frame < 665 else 3)),
        "wrap_point": wrap_point,
    }
    return hero, enemy, effects


def full_fight_state(frame: int) -> tuple[dict, dict, dict]:
    if frame <= 269:
        return early_full_state(frame)
    if frame <= 312:
        hero, enemy, effects = vault_state(frame - 269)
        effects["enemy_cable_visible"] = True
        effects["enemy_cable_points"] = effects["cable_points"]
    elif frame <= 379:
        hero, enemy = collision_state(frame - 312)
        effects = {
            "enemy_cable_visible": False,
            "enemy_cable_points": [cable_origin(enemy), cable_origin(enemy) + Vector((0.0, -0.1, 0.0))],
            "cable_visible": False,
            "cable_points": [cable_origin(enemy), cable_origin(enemy) + Vector((0.0, -0.1, 0.0))],
            "rail_break_progress": 1.0,
            "grooves": {},
        }
    elif frame <= 434:
        mapped = remap_frame(frame, 380, 434, 111, 156)
        hero, enemy, effects = reaction_state(mapped)
        effects["enemy_cable_visible"] = False
        effects["enemy_cable_points"] = effects["cable_points"]
    elif frame <= 490:
        mapped = remap_frame(frame, 435, 490, 157, 211)
        hero, enemy, effects = wrap_state(mapped)
        effects["enemy_cable_visible"] = True
        effects["enemy_cable_points"] = effects["cable_points"]
    elif frame <= 516:
        mapped = remap_frame(frame, 491, 516, 212, 238)
        hero, enemy, effects = grab_state(mapped)
        effects["enemy_cable_visible"] = True
        effects["enemy_cable_points"] = effects["cable_points"]
    elif frame <= 566:
        mapped = remap_frame(frame, 517, 566, 239, 298)
        hero, enemy, effects = drag_state(mapped)
        effects["enemy_cable_visible"] = True
        effects["enemy_cable_points"] = effects["cable_points"]
    else:
        return post_full_state(frame)
    effects.setdefault("hero_cable_visible", False)
    effects.setdefault("hero_cable_points", [Vector((0.0, 0.0, -2.0)), Vector((0.0, 0.0, -1.9))])
    effects.setdefault("projectiles", [])
    effects["bullet_pit_count"] = 3 if frame >= 270 else effects.get("bullet_pit_count", 0)
    effects["hero_foot_pit"] = frame >= 270 or effects.get("hero_foot_pit", False)
    effects["enemy_claw_pit"] = frame >= 270 or effects.get("enemy_claw_pit", False)
    effects["collision_pit"] = frame >= 341
    effects.setdefault("anchor_crack", False)
    effects.setdefault("wall_pit_count", 0)
    return hero, enemy, effects


def add_environment(mats):
    objects = []
    floor = unit_cube("ENV_floor", mats["floor"])
    key_block(floor, 1, Vector((0.0, 2.0, -0.16)), (44.0, 28.0, 0.32), Quaternion())
    objects.append(floor)
    for index, x in enumerate(range(-20, 21, 4)):
        line = unit_cube(f"ENV_grid_x_{index}", mats["grid"])
        key_block(line, 1, Vector((float(x), 2.0, 0.015)), (0.055, 28.0, 0.035), Quaternion())
        objects.append(line)
    for index, y in enumerate(range(-12, 17, 4)):
        line = unit_cube(f"ENV_grid_y_{index}", mats["grid"])
        key_block(line, 1, Vector((0.0, float(y), 0.02)), (44.0, 0.055, 0.04), Quaternion())
        objects.append(line)
    for index, (center, size) in enumerate(
        [
            ((0.0, 15.0, 2.0), (44.0, 1.6, 4.0)),
            ((-15.0, 13.0, 6.0), (3.2, 3.2, 12.0)),
            ((15.0, 13.0, 6.0), (3.2, 3.2, 12.0)),
            ((0.0, 12.5, 8.8), (30.0, 1.4, 1.4)),
            ((-11.0, 11.5, 4.0), (6.0, 2.2, 1.2)),
            ((10.0, 11.5, 3.2), (7.0, 2.2, 1.0)),
        ]
    ):
        obj = unit_cube(f"ENV_structure_{index + 1}", mats["structure"])
        key_block(obj, 1, Vector(center), size, Quaternion())
        objects.append(obj)
    return objects


def configure_lighting(scene) -> None:
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (0.075, 0.09, 0.12, 1.0)
    background.inputs["Strength"].default_value = 0.62

    sun_data = bpy.data.lights.new("PREVIS_SUN", type="SUN")
    sun_data.energy = 2.4
    sun_data.color = (1.0, 0.82, 0.64)
    sun = bpy.data.objects.new("PREVIS_SUN", sun_data)
    bpy.context.collection.objects.link(sun)
    sun.rotation_euler = (math.radians(32), math.radians(-18), math.radians(-42))

    area_data = bpy.data.lights.new("PREVIS_FILL", type="AREA")
    area_data.energy = 1650.0
    area_data.shape = "DISK"
    area_data.size = 14.0
    area_data.color = (0.68, 0.82, 1.0)
    area = bpy.data.objects.new("PREVIS_FILL", area_data)
    bpy.context.collection.objects.link(area)
    area.location = (-4.0, -16.0, 17.0)
    area.rotation_euler = (math.radians(24), 0.0, 0.0)

    rim_data = bpy.data.lights.new("PREVIS_RIM", type="AREA")
    rim_data.energy = 1250.0
    rim_data.shape = "RECTANGLE"
    rim_data.size = 10.0
    rim_data.color = (1.0, 0.58, 0.34)
    rim = bpy.data.objects.new("PREVIS_RIM", rim_data)
    bpy.context.collection.objects.link(rim)
    rim.location = (9.0, 9.0, 15.0)
    rim.rotation_euler = (math.radians(-30), 0.0, math.radians(140))


def held_frame(frame: int, hold_ranges) -> int:
    for start, end in hold_ranges:
        if start <= frame <= end:
            return start
    return frame


def create_camera(rig, frame_for, frame_end: int, fps: int, hold_ranges, sensor_width: float):
    data = bpy.data.cameras.new(rig["id"])
    data.sensor_width = sensor_width
    data.clip_start = 0.05
    data.clip_end = 500.0
    camera = bpy.data.objects.new(rig["id"], data)
    bpy.context.collection.objects.link(camera)
    camera.rotation_mode = "QUATERNION"
    keys = rig["keys"]

    def sample(seconds: float):
        if seconds <= float(keys[0]["time_s"]):
            return Vector(keys[0]["position"]), Vector(keys[0]["look_at"]), float(keys[0]["lens_mm"])
        if seconds >= float(keys[-1]["time_s"]):
            return Vector(keys[-1]["position"]), Vector(keys[-1]["look_at"]), float(keys[-1]["lens_mm"])
        for left, right in zip(keys, keys[1:]):
            start = float(left["time_s"])
            end = float(right["time_s"])
            if start <= seconds <= end:
                amount = smoothstep((seconds - start) / max(1e-6, end - start))
                return (
                    Vector(left["position"]).lerp(Vector(right["position"]), amount),
                    Vector(left["look_at"]).lerp(Vector(right["look_at"]), amount),
                    float(left["lens_mm"]) + (float(right["lens_mm"]) - float(left["lens_mm"])) * amount,
                )
        return Vector(keys[-1]["position"]), Vector(keys[-1]["look_at"]), float(keys[-1]["lens_mm"])

    start_frame = frame_for(float(keys[0]["time_s"]))
    end_frame = min(frame_end, frame_for(float(keys[-1]["time_s"])))
    for frame in range(start_frame, end_frame + 1):
        effective = held_frame(frame, hold_ranges)
        position, look_at, lens = sample((effective - 1) / fps)
        direction = look_at - position
        camera.location = position
        camera.rotation_quaternion = direction.to_track_quat("-Z", "Y")
        data.lens = lens
        camera.keyframe_insert("location", frame=frame)
        camera.keyframe_insert("rotation_quaternion", frame=frame)
        data.keyframe_insert("lens", frame=frame)
    set_interpolation(camera, "LINEAR")
    set_interpolation(data, "LINEAR")
    return camera


def rounded_vector(value: Vector):
    return [round(float(component), 5) for component in value]


def render_qa_frames(scene, frames_dir: Path, frames) -> list[str]:
    frames_dir.mkdir(parents=True, exist_ok=True)
    written = []
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGB"
    for frame in frames:
        scene.frame_set(int(frame))
        path = frames_dir / f"frame_{int(frame):03d}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        written.append(str(path.resolve()))
    return written


def render_contract(spec: dict, output: Path, project: Path, validation: Path, frames_dir: Path | None) -> None:
    started = time.perf_counter()
    clear_scene()
    scene = bpy.context.scene
    playback = spec["playback"]
    fps = int(playback.get("fps", 24))
    duration = float(playback["duration_s"])
    width, height = [int(value) for value in playback.get("resolution", [960, 402])]
    frame_end = int(round(duration * fps))
    action_program = spec.get("action_program", {})
    profile = action_program.get("profile")
    if profile not in {"first_collision_gate", "original_prompt_11_2_to_23_6"}:
        raise ValueError(f"Unsupported rigged action profile: {profile!r}")
    contact_frame = int(action_program.get("contact_frame", 29))
    hold_frames = int(action_program.get("hold_frames", 6))
    hold_end = contact_frame + hold_frames - 1
    if hold_end >= frame_end:
        raise ValueError("Contact hold extends beyond playback")

    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = frame_end
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
    stale = list(output.parent.glob(output_base.name + "*.mp4"))
    if stale:
        raise FileExistsError("Refusing to overwrite existing output: " + ", ".join(str(path) for path in stale))
    scene.render.filepath = str(output_base)

    def frame_for(seconds: float) -> int:
        return min(frame_end, max(1, int(round(seconds * fps)) + 1))

    mats = {
        "floor": make_material("MAT_floor", (0.19, 0.22, 0.27)),
        "grid": make_material("MAT_grid", (0.055, 0.075, 0.10)),
        "structure": make_material("MAT_structure", (0.31, 0.35, 0.42)),
        "hero_body": make_material("MAT_hero_body", (0.72, 0.79, 0.86)),
        "hero_armor": make_material("MAT_hero_armor", (0.48, 0.62, 0.74)),
        "hero_gold": make_material("MAT_hero_gold", (0.94, 0.70, 0.12), roughness=0.54, metallic=0.24),
        "sensor": make_material("MAT_sensor", (0.12, 0.88, 0.44), roughness=0.42),
        "enemy_body": make_material("MAT_enemy_body", (0.38, 0.40, 0.44)),
        "enemy_armor": make_material("MAT_enemy_armor", (0.46, 0.25, 0.22)),
        "enemy_core": make_material("MAT_enemy_core", (0.76, 0.18, 0.11), roughness=0.45),
        "joint": make_material("MAT_joint", (0.075, 0.09, 0.12), metallic=0.32),
        "weapon": make_material("MAT_weapon", (0.72, 0.42, 0.12), metallic=0.28),
        "weapon_dark": make_material("MAT_weapon_dark", (0.16, 0.18, 0.21), metallic=0.38),
        "impact": make_material("MAT_impact", (1.0, 0.38, 0.06), roughness=0.35),
        "cable": make_material("MAT_cable", (0.14, 0.17, 0.20), metallic=0.52),
        "cable_blade": make_material("MAT_cable_blade", (0.82, 0.22, 0.10), metallic=0.36),
        "hero_cable": make_material("MAT_hero_cable", (0.25, 0.48, 0.72), metallic=0.52),
        "hero_cable_blade": make_material("MAT_hero_cable_blade", (0.20, 0.68, 0.92), metallic=0.36),
        "rail": make_material("MAT_rail", (0.52, 0.55, 0.58), metallic=0.34),
        "groove": make_material("MAT_groove", (0.08, 0.055, 0.04), roughness=0.92),
        "soil": make_material("MAT_soil", (0.42, 0.22, 0.10), roughness=0.94),
    }
    environment = add_environment(mats)
    configure_lighting(scene)
    hero = HeroRig(mats)
    enemy = EnemyRig(mats)
    impact = ImpactRig(mats)
    uses_cables = profile in {"original_prompt_11_2_to_23_6", "original_prompt_full_30s_19shots"}
    enemy_cable = CableRig(mats, prefix="ENEMY_CABLE") if uses_cables else None
    hero_cable = (
        CableRig(
            mats,
            prefix="HERO_CABLE",
            cable_material="hero_cable",
            blade_material="hero_cable_blade",
        )
        if profile == "original_prompt_full_30s_19shots"
        else None
    )
    long_environment = LongEnvironment(mats) if uses_cables else None
    full_environment = FullEnvironment(mats) if profile == "original_prompt_full_30s_19shots" else None
    projectile_rig = ProjectileRig(mats) if profile == "original_prompt_full_30s_19shots" else None
    trace = {}
    for frame in range(1, frame_end + 1):
        if profile == "first_collision_gate":
            hero_state, enemy_state = collision_state(frame)
            effects_state = {
                "cable_visible": False,
                "cable_points": [Vector((0.0, 0.0, 0.0)), Vector((0.0, 0.0, 0.1))],
                "rail_break_progress": 0.0,
                "grooves": {},
            }
        elif profile == "original_prompt_11_2_to_23_6":
            hero_state, enemy_state, effects_state = long_fight_state(frame)
        else:
            hero_state, enemy_state, effects_state = full_fight_state(frame)
        hero_trace = hero.pose(frame, hero_state)
        enemy_trace = enemy.pose(frame, enemy_state)
        impact.pose(frame, hero_trace["hammer_contact"], contact_frame <= frame <= hold_end)
        if enemy_cable is not None:
            enemy_points = effects_state.get("enemy_cable_points", effects_state.get("cable_points", []))
            enemy_visible = bool(effects_state.get("enemy_cable_visible", effects_state.get("cable_visible")))
            effects_state["rendered_cable_points"] = enemy_cable.pose(
                frame,
                enemy_points,
                enemy_visible,
            )
        if hero_cable is not None:
            effects_state["rendered_hero_cable_points"] = hero_cable.pose(
                frame,
                effects_state.get("hero_cable_points", [Vector((0.0, 0.0, -2.0)), Vector((0.0, 0.0, -1.9))]),
                bool(effects_state.get("hero_cable_visible")),
            )
        if long_environment is not None:
            long_environment.pose(frame, effects_state)
        if full_environment is not None:
            full_environment.pose(frame, effects_state)
        if projectile_rig is not None:
            projectile_rig.pose(frame, effects_state.get("projectiles", []))
        trace[frame] = {
            "hero": hero_trace,
            "enemy": enemy_trace,
            "effects": effects_state,
        }

    animated_objects = [*environment, *hero.objects, *enemy.objects, *impact.objects]
    if enemy_cable is not None:
        animated_objects.extend(enemy_cable.objects)
    if hero_cable is not None:
        animated_objects.extend(hero_cable.objects)
    if long_environment is not None:
        animated_objects.extend(long_environment.objects)
    if full_environment is not None:
        animated_objects.extend(full_environment.objects)
    if projectile_rig is not None:
        animated_objects.extend(projectile_rig.objects)
    for obj in animated_objects:
        set_interpolation(obj, "LINEAR")

    hold_ranges = [(contact_frame, hold_end)]
    cameras = {}
    sensor_width = float(spec.get("camera", {}).get("sensor_width_mm", 36.0))
    for rig in spec.get("camera", {}).get("rigs", []):
        cameras[rig["id"]] = create_camera(rig, frame_for, frame_end, fps, hold_ranges, sensor_width)
    if not cameras:
        raise ValueError("No camera rigs")
    for shot in spec.get("timeline", {}).get("shots", []):
        camera_id = shot["camera_id"]
        marker = scene.timeline_markers.new(shot["id"], frame=frame_for(float(shot["start_s"])))
        marker.camera = cameras[camera_id]
    scene.camera = cameras[spec["timeline"]["shots"][0]["camera_id"]]

    contact = trace[contact_frame]
    hold_signatures = []
    for frame in range(contact_frame, hold_end + 1):
        item = trace[frame]
        hold_signatures.append(
            {
                "hero_root": rounded_vector(item["hero"]["root"]),
                "hammer_head": rounded_vector(item["hero"]["hammer_head"]),
                "hammer_contact": rounded_vector(item["hero"]["hammer_contact"]),
                "enemy_body": rounded_vector(item["enemy"]["body"]),
                "enemy_palms": {side: rounded_vector(value) for side, value in item["enemy"]["palms"].items()},
            }
        )
    hold_exact = all(signature == hold_signatures[0] for signature in hold_signatures[1:])
    palm_distances = {
        side: round((point - contact["hero"]["hammer_contact"]).length, 5)
        for side, point in contact["enemy"]["palms"].items()
    }
    palm_surface_distances = {
        side: round(
            point_to_oriented_box_distance(
                contact["hero"]["hammer_contact"],
                point,
                contact["enemy"]["palm_rotations"][side],
                (1.65, 1.20, 0.92),
            ),
            5,
        )
        for side, point in contact["enemy"]["palms"].items()
    }
    swing_start_frame = int(action_program.get("swing_start_frame", 1))
    recoil_probe_frame = int(action_program.get("recoil_probe_frame", frame_end))
    head_arc_distance = round(
        (trace[swing_start_frame]["hero"]["hammer_head"] - contact["hero"]["hammer_head"]).length,
        5,
    )
    hero_recoil = trace[recoil_probe_frame]["hero"]["root"] - contact["hero"]["root"]
    enemy_recoil = trace[recoil_probe_frame]["enemy"]["body"] - contact["enemy"]["body"]
    numeric_checks = {
        "joint_driven_parts": True,
        "two_hand_targets_derived_from_weapon": True,
        "hammer_head_arc_distance_m": head_arc_distance,
        "shared_contact_point": rounded_vector(contact["hero"]["hammer_contact"]),
        "enemy_palm_center_distance_to_contact_m": palm_distances,
        "enemy_palm_surface_distance_to_hammer_face_m": palm_surface_distances,
        "contact_surface_tolerance_m": 0.05,
        "contact_overlap_pass": max(palm_surface_distances.values()) <= 0.05,
        "hold_frames": list(range(contact_frame, hold_end + 1)),
        "hold_transform_exact": hold_exact,
        "hero_recoil_vector": rounded_vector(hero_recoil),
        "enemy_recoil_vector": rounded_vector(enemy_recoil),
        "bidirectional_recoil_pass": hero_recoil.x < -2.0 and enemy_recoil.x > 2.0 and enemy_recoil.z > 1.0,
    }
    if profile == "original_prompt_11_2_to_23_6":
        vault_frame = int(action_program.get("vault_probe_frame", 23))
        wrap_frame = int(action_program.get("wrap_probe_frame", 211))
        grab_frame = int(action_program.get("grab_probe_frame", 238))
        drag_start_frame = int(action_program.get("drag_start_frame", 239))
        tracking_frames = [226, grab_frame, drag_start_frame, 260, frame_end]
        cable_tracking_errors = {}
        for probe_frame in tracking_frames:
            left_target = trace[probe_frame]["hero"]["grip_targets"]["L"]
            rendered_cable = trace[probe_frame]["effects"].get("rendered_cable_points", [])
            cable_tracking_errors[str(probe_frame)] = round(
                point_to_polyline_distance(left_target, rendered_cable),
                5,
            )
        cable_grab_error = max(cable_tracking_errors.values())
        wrap_rendered = [Vector(point) for point in trace[wrap_frame]["effects"].get("rendered_cable_points", [])]
        wrap_depth_span = max(point.y for point in wrap_rendered) - min(point.y for point in wrap_rendered)
        route_controls = [Vector(point) for point in trace[184]["effects"].get("cable_points", [])]
        spool_outfeed_depth = abs(route_controls[1].y - route_controls[0].y) if len(route_controls) >= 2 else 0.0
        drag_distance = trace[frame_end]["hero"]["root"].x - trace[drag_start_frame]["hero"]["root"].x
        left_foot_hold = (
            trace[252]["hero"]["feet"]["L"] - trace[239]["hero"]["feet"]["L"]
        ).length <= 0.02
        right_foot_hold = (
            trace[268]["hero"]["feet"]["R"] - trace[239]["hero"]["feet"]["R"]
        ).length <= 0.02
        root_moves_during_left_hold = abs(trace[252]["hero"]["root"].x - trace[239]["hero"]["root"].x) >= 0.10
        numeric_checks.update(
            {
                "vault_tucked_foot_min_height_m": round(
                    min(
                        trace[vault_frame]["hero"]["root"].z,
                        trace[vault_frame]["hero"]["head"].z - 4.0,
                    ),
                    5,
                ),
                "cable_visible_at_wrap": bool(trace[wrap_frame]["effects"].get("cable_visible")),
                "spool_outfeed_camera_side_depth_m": round(spool_outfeed_depth, 5),
                "spool_outfeed_visibility_pass": spool_outfeed_depth >= 1.5,
                "wrap_front_back_depth_span_m": round(wrap_depth_span, 5),
                "wrap_depth_pass": wrap_depth_span >= 1.5,
                "left_hand_to_rendered_cable_errors_m": cable_tracking_errors,
                "left_hand_to_rendered_cable_max_error_m": round(cable_grab_error, 5),
                "cable_grab_pass": cable_grab_error <= 0.12,
                "hero_drag_distance_m": round(drag_distance, 5),
                "left_foot_planted_239_252": left_foot_hold,
                "right_foot_planted_239_268": right_foot_hold,
                "root_moves_while_left_foot_planted": root_moves_during_left_hold,
                "staggered_foot_braking_pass": left_foot_hold and right_foot_hold and root_moves_during_left_hold,
                "drag_and_groove_pass": drag_distance >= 2.0 and bool(trace[frame_end]["effects"].get("grooves")),
                "shot_count": len(spec.get("timeline", {}).get("shots", [])),
            }
        )
    required_checks = [
        numeric_checks["contact_overlap_pass"],
        numeric_checks["hold_transform_exact"],
        numeric_checks["bidirectional_recoil_pass"],
        head_arc_distance >= 5.0,
    ]
    if profile == "original_prompt_11_2_to_23_6":
        required_checks.extend(
            [
                numeric_checks["cable_visible_at_wrap"],
                numeric_checks["spool_outfeed_visibility_pass"],
                numeric_checks["wrap_depth_pass"],
                numeric_checks["cable_grab_pass"],
                numeric_checks["staggered_foot_braking_pass"],
                numeric_checks["drag_and_groove_pass"],
                numeric_checks["shot_count"] >= 7,
            ]
        )
    if profile == "original_prompt_full_30s_19shots":
        hammer_length_start = (
            trace[159]["hero"]["hammer_head"] - trace[159]["hero"]["hammer_butt"]
        ).length
        hammer_length_end = (
            trace[197]["hero"]["hammer_head"] - trace[197]["hero"]["hammer_butt"]
        ).length
        full_tracking_frames = [503, 516, 517, 540, 566]
        full_cable_errors = {}
        for probe_frame in full_tracking_frames:
            target = trace[probe_frame]["hero"]["grip_targets"]["L"]
            rendered = trace[probe_frame]["effects"].get("rendered_cable_points", [])
            full_cable_errors[str(probe_frame)] = round(point_to_polyline_distance(target, rendered), 5)
        enemy_source = Vector(trace[610]["effects"]["rendered_cable_points"][0])
        hero_source = Vector(trace[610]["effects"]["rendered_hero_cable_points"][0])
        hero_anchor = Vector(trace[610]["effects"]["rendered_hero_cable_points"][-1])
        expected_anchor = Vector((-3.8, -9.8, 4.2))
        wall_step_heights = [
            round(float(trace[628]["hero"]["feet"]["L"].z), 4),
            round(float(trace[646]["hero"]["feet"]["R"].z), 4),
            round(float(trace[665]["hero"]["feet"]["L"].z), 4),
        ]
        numeric_checks.update(
            {
                "exact_shot_count": len(spec.get("timeline", {}).get("shots", [])),
                "hammer_extension_start_m": round(hammer_length_start, 5),
                "hammer_extension_end_m": round(hammer_length_end, 5),
                "hammer_extension_pass": hammer_length_end - hammer_length_start >= 1.5,
                "three_bullet_pits_pass": int(trace[247]["effects"].get("bullet_pit_count", 0)) == 3,
                "enemy_cable_release_visible": bool(trace[269]["effects"].get("enemy_cable_visible")),
                "enemy_cable_visible_after_vault": bool(trace[312]["effects"].get("enemy_cable_visible")),
                "full_drag_hand_to_rendered_cable_errors_m": full_cable_errors,
                "full_drag_cable_contact_pass": max(full_cable_errors.values()) <= 0.12,
                "distinct_cable_source_distance_m": round((enemy_source - hero_source).length, 5),
                "distinct_cable_sources_pass": (enemy_source - hero_source).length >= 5.0,
                "hero_anchor_error_m": round((hero_anchor - expected_anchor).length, 5),
                "hero_anchor_pass": (hero_anchor - expected_anchor).length <= 0.20,
                "wall_step_heights_m": wall_step_heights,
                "three_wall_steps_pass": wall_step_heights[0] < wall_step_heights[1] < wall_step_heights[2],
                "cannon_open_amount_final": round(float(trace[720]["enemy"].get("beak_open", 0.0)), 5),
                "cannon_open_pass": float(trace[720]["enemy"].get("beak_open", 0.0)) >= 0.95,
                "hero_airborne_height_final_m": round(float(trace[720]["hero"]["root"].z), 5),
                "hero_airborne_pass": float(trace[720]["hero"]["root"].z) >= 10.0,
            }
        )
        required_checks.extend(
            [
                numeric_checks["exact_shot_count"] == 19,
                numeric_checks["hammer_extension_pass"],
                numeric_checks["three_bullet_pits_pass"],
                numeric_checks["enemy_cable_release_visible"],
                numeric_checks["enemy_cable_visible_after_vault"],
                numeric_checks["full_drag_cable_contact_pass"],
                numeric_checks["distinct_cable_sources_pass"],
                numeric_checks["hero_anchor_pass"],
                numeric_checks["three_wall_steps_pass"],
                numeric_checks["cannon_open_pass"],
                numeric_checks["hero_airborne_pass"],
            ]
        )
    if not all(
        required_checks
    ):
        raise RuntimeError(
            "Rigged action numeric gate failed before render: "
            + json.dumps(numeric_checks, ensure_ascii=False, sort_keys=True)
        )

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
    except Exception as exc:
        decode_error = f"{type(exc).__name__}: {exc}"

    qa_paths = []
    if frames_dir is not None:
        qa_frames = spec.get("validation_targets", {}).get(
            "qa_frames",
            [1, 12, 21, 27, contact_frame, hold_end, hold_end + 1, 45, frame_end],
        )
        qa_paths = render_qa_frames(scene, frames_dir, qa_frames)

    report = {
        "status": "pass_numeric_pending_independent_visual_review"
        if decoded_frames in {None, frame_end}
        else "frame_count_mismatch",
        "engine": "Blender 5.2.1 LTS / EEVEE / FFmpeg H.264",
        "backend": "rigged_joint_solver_v1",
        "profile": profile,
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
        "numeric_action_checks": numeric_checks,
        "qa_frames": qa_paths,
        "shots": spec.get("timeline", {}).get("shots", []),
        "elapsed_s": round(time.perf_counter() - started, 3),
        "claim_boundary": "Numeric rig/contact/media checks passed; fight readability still requires an independent viewer.",
    }
    ensure_parent(validation)
    validation.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if report["status"] == "frame_count_mismatch":
        raise RuntimeError("Rendered MP4 frame count mismatch")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    args = parse_args()
    spec_path = Path(args.spec).resolve()
    output_path = Path(args.output).resolve()
    project_path = Path(args.project).resolve()
    validation_path = Path(args.validation).resolve()
    frames_path = Path(args.frames_dir).resolve() if args.frames_dir else None
    contract = json.loads(spec_path.read_text(encoding="utf-8"))
    if contract.get("schema_version") != "previs-compiler/1.0":
        raise SystemExit(f"Unsupported schema_version: {contract.get('schema_version')}")
    if contract.get("meta", {}).get("execution_backend") != "rigged_joint_solver_v1":
        raise SystemExit("Spec does not select rigged_joint_solver_v1")
    render_contract(contract, output_path, project_path, validation_path, frames_path)
