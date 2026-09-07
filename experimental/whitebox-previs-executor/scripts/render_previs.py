#!/usr/bin/env python3
"""Dependency-free software 3D renderer for playable whitebox previs MP4s."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

from validate_spec import validate


Vec3 = tuple[float, float, float]
Color = tuple[int, int, int]


@dataclass
class Camera:
    position: Vec3
    look_at: Vec3
    lens_mm: float


@dataclass
class Primitive:
    depth: float
    kind: str
    points: list[tuple[float, float]]
    color: Color
    width: int = 1
    outline: Color | None = None


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def mix(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix_vec(a: Sequence[float], b: Sequence[float], t: float) -> Vec3:
    return (mix(a[0], b[0], t), mix(a[1], b[1], t), mix(a[2], b[2], t))


def smoothstep(t: float) -> float:
    t = clamp(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def sub(a: Sequence[float], b: Sequence[float]) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a: Sequence[float], b: Sequence[float]) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def scale(a: Sequence[float], value: float) -> Vec3:
    return (a[0] * value, a[1] * value, a[2] * value)


def dot(a: Sequence[float], b: Sequence[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Sequence[float], b: Sequence[float]) -> Vec3:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def length(a: Sequence[float]) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: Sequence[float]) -> Vec3:
    size = length(a)
    if size < 1e-9:
        return (0.0, 1.0, 0.0)
    return (a[0] / size, a[1] / size, a[2] / size)


def camera_basis(camera: Camera) -> tuple[Vec3, Vec3, Vec3]:
    forward = normalize(sub(camera.look_at, camera.position))
    world_up = (0.0, 0.0, 1.0)
    right = normalize(cross(forward, world_up))
    if length(right) < 1e-6:
        right = (1.0, 0.0, 0.0)
    up = normalize(cross(right, forward))
    return right, up, forward


def project(point: Sequence[float], camera: Camera, width: int, height: int) -> tuple[float, float, float] | None:
    right, up, forward = camera_basis(camera)
    relative = sub(point, camera.position)
    depth = dot(relative, forward)
    if depth <= 0.08:
        return None
    x = dot(relative, right)
    y = dot(relative, up)
    focal_px = (width * 0.5) * camera.lens_mm / 18.0
    return (width * 0.5 + focal_px * x / depth, height * 0.5 - focal_px * y / depth, depth)


class Raster:
    def __init__(self, width: int, height: int, background: Color = (18, 21, 26)) -> None:
        self.width = width
        self.height = height
        self.buffer = bytearray(bytes(background) * (width * height))

    def _span(self, y: int, x0: int, x1: int, color: Color) -> None:
        if y < 0 or y >= self.height:
            return
        x0 = max(0, min(self.width - 1, x0))
        x1 = max(0, min(self.width - 1, x1))
        if x1 < x0:
            x0, x1 = x1, x0
        start = (y * self.width + x0) * 3
        self.buffer[start : start + (x1 - x0 + 1) * 3] = bytes(color) * (x1 - x0 + 1)

    def polygon(self, points: Sequence[tuple[float, float]], color: Color, outline: Color | None = None) -> None:
        if len(points) < 3:
            return
        min_y = max(0, int(math.floor(min(p[1] for p in points))))
        max_y = min(self.height - 1, int(math.ceil(max(p[1] for p in points))))
        for y in range(min_y, max_y + 1):
            scan_y = y + 0.5
            intersections: list[float] = []
            for index, p1 in enumerate(points):
                p2 = points[(index + 1) % len(points)]
                if (p1[1] <= scan_y < p2[1]) or (p2[1] <= scan_y < p1[1]):
                    ratio = (scan_y - p1[1]) / (p2[1] - p1[1])
                    intersections.append(p1[0] + (p2[0] - p1[0]) * ratio)
            intersections.sort()
            for index in range(0, len(intersections) - 1, 2):
                self._span(y, int(math.ceil(intersections[index])), int(math.floor(intersections[index + 1])), color)
        if outline:
            for index, p1 in enumerate(points):
                self.line(p1, points[(index + 1) % len(points)], outline, 1)

    def disc(self, center: tuple[float, float], radius: int, color: Color, outline: Color | None = None) -> None:
        cx, cy = int(round(center[0])), int(round(center[1]))
        radius = max(1, radius)
        for dy in range(-radius, radius + 1):
            span = int(math.sqrt(max(0, radius * radius - dy * dy)))
            self._span(cy + dy, cx - span, cx + span, color)
        if outline:
            steps = max(12, radius * 3)
            previous = None
            first = None
            for i in range(steps + 1):
                angle = 2 * math.pi * i / steps
                point = (cx + math.cos(angle) * radius, cy + math.sin(angle) * radius)
                if first is None:
                    first = point
                if previous is not None:
                    self.line(previous, point, outline, 1)
                previous = point

    def line(self, a: tuple[float, float], b: tuple[float, float], color: Color, width: int = 1) -> None:
        x0, y0 = a
        x1, y1 = b
        dx, dy = x1 - x0, y1 - y0
        if width > 2:
            segment_length = math.hypot(dx, dy)
            if segment_length < 1e-6:
                self.disc(a, max(1, width // 2), color)
                return
            half = width * 0.5
            px, py = -dy / segment_length * half, dx / segment_length * half
            self.polygon(
                [(x0 + px, y0 + py), (x1 + px, y1 + py), (x1 - px, y1 - py), (x0 - px, y0 - py)],
                color,
            )
            self.disc(a, max(1, width // 2), color)
            self.disc(b, max(1, width // 2), color)
            return
        steps = max(1, int(max(abs(dx), abs(dy))))
        for index in range(steps + 1):
            t = index / steps
            x = int(round(mix(x0, x1, t)))
            y = int(round(mix(y0, y1, t)))
            if 0 <= x < self.width and 0 <= y < self.height:
                offset = (y * self.width + x) * 3
                self.buffer[offset : offset + 3] = bytes(color)

    def rect(self, x: int, y: int, width: int, height: int, color: Color) -> None:
        for row in range(max(0, y), min(self.height, y + height)):
            self._span(row, x, x + width - 1, color)


FONT = {
    "0": ["111", "101", "101", "101", "111"], "1": ["010", "110", "010", "010", "111"],
    "2": ["111", "001", "111", "100", "111"], "3": ["111", "001", "111", "001", "111"],
    "4": ["101", "101", "111", "001", "001"], "5": ["111", "100", "111", "001", "111"],
    "6": ["111", "100", "111", "101", "111"], "7": ["111", "001", "010", "010", "010"],
    "8": ["111", "101", "111", "101", "111"], "9": ["111", "101", "111", "001", "111"],
    "A": ["010", "101", "111", "101", "101"], "C": ["111", "100", "100", "100", "111"],
    "D": ["110", "101", "101", "101", "110"], "E": ["111", "100", "110", "100", "111"],
    "H": ["101", "101", "111", "101", "101"], "I": ["111", "010", "010", "010", "111"],
    "L": ["100", "100", "100", "100", "111"], "M": ["101", "111", "111", "101", "101"],
    "O": ["111", "101", "101", "101", "111"], "R": ["110", "101", "110", "101", "101"],
    "S": ["111", "100", "111", "001", "111"], "T": ["111", "010", "010", "010", "010"],
    "W": ["101", "101", "111", "111", "101"], "-": ["000", "000", "111", "000", "000"],
    ".": ["000", "000", "000", "000", "010"], ":": ["000", "010", "000", "010", "000"],
    "/": ["001", "001", "010", "100", "100"], " ": ["000", "000", "000", "000", "000"],
}


def draw_text(raster: Raster, text: str, x: int, y: int, scale_value: int, color: Color) -> None:
    cursor = x
    for char in text.upper():
        pattern = FONT.get(char, FONT[" "])
        for row, bits in enumerate(pattern):
            for column, bit in enumerate(bits):
                if bit == "1":
                    raster.rect(cursor + column * scale_value, y + row * scale_value, scale_value, scale_value, color)
        cursor += 4 * scale_value


def keyframe_pair(keyframes: list[dict], time_value: float) -> tuple[dict, dict, float]:
    if time_value <= keyframes[0]["time"]:
        return keyframes[0], keyframes[0], 0.0
    if time_value >= keyframes[-1]["time"]:
        return keyframes[-1], keyframes[-1], 0.0
    for index in range(len(keyframes) - 1):
        left, right = keyframes[index], keyframes[index + 1]
        if left["time"] <= time_value <= right["time"]:
            ratio = (time_value - left["time"]) / max(1e-9, right["time"] - left["time"])
            if right.get("easing", left.get("easing", "smooth")) == "smooth":
                ratio = smoothstep(ratio)
            return left, right, ratio
    return keyframes[-1], keyframes[-1], 0.0


def camera_at(shot: dict, time_value: float) -> Camera:
    left, right, ratio = keyframe_pair(shot["camera_keyframes"], time_value)
    return Camera(
        mix_vec(left["position"], right["position"], ratio),
        mix_vec(left["look_at"], right["look_at"], ratio),
        mix(float(left.get("lens_mm", 35)), float(right.get("lens_mm", 35)), ratio),
    )


def actor_at(actor: dict, time_value: float) -> tuple[Vec3, float, str, float, float]:
    left, right, ratio = keyframe_pair(actor["keyframes"], time_value)
    position = mix_vec(left["position"], right["position"], ratio)
    facing = mix(float(left.get("facing", 0)), float(right.get("facing", left.get("facing", 0))), ratio)
    distance = length(sub(right["position"], left["position"]))
    moving = distance > 0.02 and left is not right
    action = right.get("action", left.get("action", "walk" if moving else "idle"))
    phase = (time_value * (5.5 if action == "run" else 3.2)) % (2 * math.pi)
    progress = ratio if left is not right else 1.0
    return position, facing, action, phase, progress


BOX_VERTICES = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (-0.5, 0.5, 0.5),
]
BOX_FACES = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]


def add_box(primitives: list[Primitive], center: Sequence[float], size: Sequence[float], camera: Camera, width: int, height: int, base: Color) -> None:
    vertices = [
        (center[0] + v[0] * size[0], center[1] + v[1] * size[1], center[2] + v[2] * size[2])
        for v in BOX_VERTICES
    ]
    projected = [project(vertex, camera, width, height) for vertex in vertices]
    for face_index, face in enumerate(BOX_FACES):
        if any(projected[index] is None for index in face):
            continue
        values = [projected[index] for index in face]
        points = [(value[0], value[1]) for value in values if value]
        depth = sum(value[2] for value in values if value) / len(values)
        shade = 0.78 + face_index * 0.035
        color = tuple(int(clamp(channel * shade, 0, 255)) for channel in base)
        primitives.append(Primitive(depth, "polygon", points, color, outline=(70, 76, 84)))


def rotate_xy(point: Vec3, yaw_degrees: float) -> Vec3:
    angle = math.radians(yaw_degrees)
    sin_a, cos_a = math.sin(angle), math.cos(angle)
    return (point[0] * cos_a + point[1] * sin_a, -point[0] * sin_a + point[1] * cos_a, point[2])


def world_point(origin: Sequence[float], local: Vec3, yaw: float) -> Vec3:
    return add(origin, rotate_xy(local, yaw))


def add_hover_actor(primitives: list[Primitive], actor: dict, time_value: float, camera: Camera, width: int, height: int) -> None:
    position, facing, action, phase, action_progress = actor_at(actor, time_value)
    actor_height = float(actor.get("height", 20))
    span = float(actor.get("span", actor_height * 1.35))
    tone = int(clamp(float(actor.get("tone", 0.7)) * 255, 70, 245))
    color = (tone, tone, min(255, tone + 5))
    outline = (42, 46, 52)
    body_z = actor_height * 0.54
    body_y = actor_height * 0.04
    if action == "recoil":
        body_y -= actor_height * 0.18 * smoothstep(action_progress)
        body_z += actor_height * 0.08 * smoothstep(action_progress)
    left_contact = (-span * 0.42, 0.25 * actor_height, 0.08)
    right_contact = (span * 0.42, 0.25 * actor_height, 0.08)
    if action in {"dash", "run"}:
        swing = math.sin(phase) * actor_height * 0.2
        left_contact = (-span * 0.42, actor_height * 0.2 + swing, 0.08)
        right_contact = (span * 0.42, actor_height * 0.2 - swing, 0.08)
    elif action == "block":
        left_contact = (-span * 0.32, actor_height * 0.55, actor_height * 0.28)
        right_contact = (span * 0.28, actor_height * 0.48, actor_height * 0.34)
    elif action == "thrust":
        right_contact = (span * 0.18, actor_height * 0.78, actor_height * 0.4)

    local_points = {
        "body": (0, body_y, body_z),
        "head": (0, actor_height * 0.28 + body_y, body_z + actor_height * 0.02),
        "lshoulder": (-span * 0.35, body_y, body_z + actor_height * 0.05),
        "rshoulder": (span * 0.35, body_y, body_z + actor_height * 0.05),
        "lelbow": (-span * 0.45, actor_height * 0.13, actor_height * 0.32),
        "relbow": (span * 0.45, actor_height * 0.13, actor_height * 0.32),
        "lclaw": left_contact,
        "rclaw": right_contact,
    }
    world = {name: world_point(position, point, facing) for name, point in local_points.items()}
    projected = {name: project(point, camera, width, height) for name, point in world.items()}
    segments = [
        ("body", "lshoulder", 0.16), ("lshoulder", "lelbow", 0.14), ("lelbow", "lclaw", 0.11),
        ("body", "rshoulder", 0.16), ("rshoulder", "relbow", 0.14), ("relbow", "rclaw", 0.11),
    ]
    for start_name, end_name, thickness_ratio in segments:
        start, end = projected[start_name], projected[end_name]
        if not start or not end:
            continue
        depth = (start[2] + end[2]) * 0.5
        pixels = max(3, int((width * 0.5 * camera.lens_mm / 18.0) * actor_height * thickness_ratio * 0.1 / depth))
        primitives.append(Primitive(depth, "line", [(start[0], start[1]), (end[0], end[1])], color, pixels, outline))
    for name, radius_ratio in (("body", 0.18), ("head", 0.08), ("lclaw", 0.055), ("rclaw", 0.055)):
        value = projected[name]
        if not value:
            continue
        radius = max(4, int((width * 0.5 * camera.lens_mm / 18.0) * actor_height * radius_ratio / value[2]))
        primitives.append(Primitive(value[2], "disc", [(value[0], value[1]), (radius, 0)], color, 1, outline))


def add_actor(primitives: list[Primitive], actor: dict, time_value: float, camera: Camera, width: int, height: int) -> None:
    if actor.get("rig", "humanoid") == "two-arm-hover":
        add_hover_actor(primitives, actor, time_value, camera, width, height)
        return
    position, facing, action, phase, action_progress = actor_at(actor, time_value)
    actor_height = float(actor.get("height", 1.75))
    tone = int(clamp(float(actor.get("tone", 0.9)) * 255, 80, 250))
    color = (tone, tone, min(255, tone + 4))
    outline = (42, 46, 52)
    locomotion = action in {"walk", "run", "dash"}
    stride_scale = 0.12 if action == "walk" else 0.2 if action == "run" else 0.28
    stride = math.sin(phase) * actor_height * stride_scale if locomotion else 0.0
    arm_stride = -stride * 0.85
    hip_z = actor_height * (0.5 if action != "sit" else 0.38)
    shoulder_z = actor_height * (0.76 if action != "sit" else 0.62)
    head_z = actor_height * (0.91 if action != "sit" else 0.77)
    joints = {
        "hip": (0, 0, hip_z), "shoulder": (0, 0, shoulder_z), "head": (0, 0, head_z),
        "lknee": (-0.11, stride * 0.35, actor_height * 0.27), "rknee": (0.11, -stride * 0.35, actor_height * 0.27),
        "lfoot": (-0.12, stride, 0.04), "rfoot": (0.12, -stride, 0.04),
        "lelbow": (-0.25, arm_stride * 0.35, actor_height * 0.61), "relbow": (0.25, -arm_stride * 0.35, actor_height * 0.61),
        "lhand": (-0.3, arm_stride, actor_height * 0.46), "rhand": (0.3, -arm_stride, actor_height * 0.46),
    }
    if action == "reach":
        joints["relbow"] = (0.18, 0.2, actor_height * 0.7)
        joints["rhand"] = (0.12, 0.58, actor_height * 0.72)
    elif action == "dash":
        lean = actor_height * 0.12
        joints["shoulder"] = (0, lean, shoulder_z - actor_height * 0.04)
        joints["head"] = (0, lean * 1.35, head_z - actor_height * 0.05)
        joints["lelbow"] = (-0.22, -0.2, actor_height * 0.62)
        joints["relbow"] = (0.22, -0.2, actor_height * 0.62)
        joints["lhand"] = (-0.28, -0.5, actor_height * 0.5)
        joints["rhand"] = (0.28, -0.5, actor_height * 0.5)
    elif action == "guard":
        joints["lelbow"] = (-0.32, 0.18, actor_height * 0.66)
        joints["relbow"] = (0.32, 0.2, actor_height * 0.68)
        joints["lhand"] = (-0.2, 0.46, actor_height * 0.63)
        joints["rhand"] = (0.2, 0.48, actor_height * 0.7)
        joints["lfoot"] = (-0.25, -0.12, 0.04)
        joints["rfoot"] = (0.25, 0.12, 0.04)
    elif action == "block":
        joints["lelbow"] = (-0.3, 0.26, actor_height * 0.72)
        joints["relbow"] = (0.3, 0.25, actor_height * 0.7)
        joints["lhand"] = (-0.08, 0.5, actor_height * 0.78)
        joints["rhand"] = (0.1, 0.5, actor_height * 0.64)
        joints["lfoot"] = (-0.3, -0.15, 0.04)
        joints["rfoot"] = (0.3, 0.15, 0.04)
    elif action in {"slash", "slash_hold"}:
        p = 1.0 if action == "slash_hold" else smoothstep(action_progress)
        joints["relbow"] = mix_vec((0.38, 0.0, actor_height * 0.82), (-0.18, 0.42, actor_height * 0.58), p)
        joints["rhand"] = mix_vec((0.5, 0.08, actor_height * 0.93), (-0.42, 0.7, actor_height * 0.42), p)
        joints["lelbow"] = mix_vec((-0.2, -0.08, actor_height * 0.68), (0.12, 0.3, actor_height * 0.6), p)
        joints["lhand"] = mix_vec((-0.28, -0.2, actor_height * 0.56), (-0.2, 0.5, actor_height * 0.52), p)
        joints["shoulder"] = (0, actor_height * 0.05 * p, shoulder_z - actor_height * 0.04 * p)
    elif action == "thrust":
        p = smoothstep(action_progress)
        joints["relbow"] = mix_vec((0.28, 0.1, actor_height * 0.7), (0.08, 0.55, actor_height * 0.67), p)
        joints["rhand"] = mix_vec((0.3, 0.25, actor_height * 0.68), (0.02, 0.95, actor_height * 0.66), p)
        joints["lhand"] = (-0.2, 0.38, actor_height * 0.62)
        joints["shoulder"] = (0, actor_height * 0.08 * p, shoulder_z)
    elif action == "recoil":
        p = smoothstep(action_progress)
        joints["shoulder"] = (0, -actor_height * 0.16 * p, shoulder_z - actor_height * 0.05 * p)
        joints["head"] = (0, -actor_height * 0.23 * p, head_z - actor_height * 0.08 * p)
        joints["lelbow"] = (-0.35, -0.18, actor_height * 0.66)
        joints["relbow"] = (0.35, -0.16, actor_height * 0.66)
        joints["lhand"] = (-0.5, -0.35, actor_height * 0.54)
        joints["rhand"] = (0.5, -0.32, actor_height * 0.54)
    world = {name: world_point(position, point, facing) for name, point in joints.items()}
    projected = {name: project(point, camera, width, height) for name, point in world.items()}
    segments = [
        ("hip", "shoulder", 0.105), ("hip", "lknee", 0.06), ("lknee", "lfoot", 0.045),
        ("hip", "rknee", 0.06), ("rknee", "rfoot", 0.045), ("shoulder", "lelbow", 0.05),
        ("lelbow", "lhand", 0.04), ("shoulder", "relbow", 0.05), ("relbow", "rhand", 0.04),
    ]
    for start_name, end_name, thickness_world in segments:
        start, end = projected[start_name], projected[end_name]
        if not start or not end:
            continue
        depth = (start[2] + end[2]) * 0.5
        body_scale = max(0.2, actor_height / 1.75 * float(actor.get("limb_scale", 1.0)))
        pixels = max(2, int((width * 0.5 * camera.lens_mm / 18.0) * thickness_world * body_scale / depth))
        primitives.append(Primitive(depth, "line", [(start[0], start[1]), (end[0], end[1])], color, pixels, outline))
    head = projected["head"]
    if head:
        head_ratio = float(actor.get("head_ratio", 0.09))
        radius = max(3, int((width * 0.5 * camera.lens_mm / 18.0) * actor_height * head_ratio / head[2]))
        primitives.append(Primitive(head[2], "disc", [(head[0], head[1]), (radius, 0)], color, 1, outline))

    weapon = actor.get("weapon")
    if isinstance(weapon, dict) and weapon.get("type") in {"sword", "hammer"}:
        blade_length = float(weapon.get("length", actor_height * 0.7))
        hand_local = joints["rhand"]
        if action == "block":
            direction = normalize((-0.72, 0.2, 0.68))
        elif action in {"slash", "slash_hold"}:
            direction = normalize((-0.78, 0.72, -0.28))
        elif action == "thrust":
            direction = (0.0, 1.0, 0.0)
        elif action == "recoil":
            direction = normalize((0.55, -0.35, 0.62))
        else:
            direction = normalize((0.25, 0.72, 0.64))
        blade_end_local = add(hand_local, scale(direction, blade_length))
        blade_start_world = world["rhand"]
        blade_end_world = world_point(position, blade_end_local, facing)
        blade_start = project(blade_start_world, camera, width, height)
        blade_end = project(blade_end_world, camera, width, height)
        if blade_start and blade_end:
            depth = (blade_start[2] + blade_end[2]) * 0.5
            pixels = max(2, int((width * 0.5 * camera.lens_mm / 18.0) * actor_height * 0.025 / depth))
            primitives.append(
                Primitive(
                    depth,
                    "line",
                    [(blade_start[0], blade_start[1]), (blade_end[0], blade_end[1])],
                    (238, 247, 255),
                    pixels,
                    (92, 124, 146),
                )
            )
            if weapon.get("type") == "hammer":
                head_size = weapon.get("head_size", [actor_height * 0.22, actor_height * 0.12, actor_height * 0.12])
                add_box(primitives, blade_end_world, head_size, camera, width, height, (184, 190, 198))


def tether_endpoint(endpoint: dict, actors: dict[str, dict], time_value: float) -> Vec3 | None:
    if "world" in endpoint:
        value = endpoint["world"]
        return (float(value[0]), float(value[1]), float(value[2]))
    actor_id = endpoint.get("actor")
    actor = actors.get(actor_id)
    if not actor:
        return None
    position, facing, _action, _phase, _progress = actor_at(actor, time_value)
    offset = endpoint.get("offset", [0, 0, 0])
    return world_point(position, (float(offset[0]), float(offset[1]), float(offset[2])), facing)


def add_tethers(primitives: list[Primitive], tethers: list[dict], actors: list[dict], time_value: float, camera: Camera, width: int, height: int) -> None:
    actor_map = {actor["id"]: actor for actor in actors}
    for tether in tethers:
        if not float(tether.get("start", 0)) <= time_value <= float(tether.get("end", 0)):
            continue
        start_world = tether_endpoint(tether.get("from", {}), actor_map, time_value)
        end_world = tether_endpoint(tether.get("to", {}), actor_map, time_value)
        if not start_world or not end_world:
            continue
        start = project(start_world, camera, width, height)
        end = project(end_world, camera, width, height)
        if not start or not end:
            continue
        depth = (start[2] + end[2]) * 0.5
        tone = int(clamp(float(tether.get("tone", 0.85)) * 255, 80, 250))
        primitives.append(Primitive(depth, "line", [(start[0], start[1]), (end[0], end[1])], (tone, tone, min(255, tone + 5)), 3, (45, 52, 60)))


def add_effects(primitives: list[Primitive], effects: list[dict], time_value: float, camera: Camera, width: int, height: int) -> None:
    for effect in effects:
        if effect.get("type") != "impact":
            continue
        start = float(effect.get("time", 0))
        duration = max(0.01, float(effect.get("duration", 0.2)))
        if not start <= time_value <= start + duration:
            continue
        center = project(effect.get("position", [0, 0, 1]), camera, width, height)
        if not center:
            continue
        envelope = 1.0 if effect.get("hold", False) else math.sin(math.pi * (time_value - start) / duration)
        radius_world = float(effect.get("radius", 1)) * max(0.15, envelope)
        radius_px = max(3, int((width * 0.5 * camera.lens_mm / 18.0) * radius_world / center[2]))
        for index in range(8):
            angle = math.pi * index / 4
            inner = radius_px * 0.25
            outer = radius_px
            primitives.append(
                Primitive(
                    max(0.01, center[2] - 0.02),
                    "line",
                    [
                        (center[0] + math.cos(angle) * inner, center[1] + math.sin(angle) * inner),
                        (center[0] + math.cos(angle) * outer, center[1] + math.sin(angle) * outer),
                    ],
                    (255, 255, 255),
                    max(2, radius_px // 16),
                    (112, 150, 176),
                )
            )


def add_grid(primitives: list[Primitive], floor: dict, camera: Camera, width: int, height: int) -> None:
    size = floor.get("size", [12, 10])
    grid = max(0.25, float(floor.get("grid", 1)))
    x_half, y_half = size[0] * 0.5, size[1] * 0.5
    x = -x_half
    while x <= x_half + 1e-6:
        start, end = project((x, -y_half, 0), camera, width, height), project((x, y_half, 0), camera, width, height)
        if start and end:
            primitives.append(Primitive((start[2] + end[2]) * 0.5, "line", [(start[0], start[1]), (end[0], end[1])], (43, 48, 56)))
        x += grid
    y = -y_half
    while y <= y_half + 1e-6:
        start, end = project((-x_half, y, 0), camera, width, height), project((x_half, y, 0), camera, width, height)
        if start and end:
            primitives.append(Primitive((start[2] + end[2]) * 0.5, "line", [(start[0], start[1]), (end[0], end[1])], (43, 48, 56)))
        y += grid


def active_shot(shots: list[dict], time_value: float) -> dict:
    for shot in shots:
        if shot["start"] <= time_value < shot["end"]:
            return shot
    return shots[-1]


def render_frame(data: dict, time_value: float) -> bytes:
    width, height = data["resolution"]
    shot = active_shot(data["shots"], time_value)
    camera = camera_at(shot, time_value)
    primitives: list[Primitive] = []
    add_grid(primitives, data.get("world", {}).get("floor", {}), camera, width, height)
    for wall in data.get("world", {}).get("walls", []):
        add_box(primitives, wall["center"], wall["size"], camera, width, height, (126, 132, 141))
    for prop in data.get("world", {}).get("props", []):
        add_box(primitives, prop["center"], prop["size"], camera, width, height, (104, 111, 121))
    for actor in data.get("actors", []):
        add_actor(primitives, actor, time_value, camera, width, height)
    add_tethers(primitives, data.get("tethers", []), data.get("actors", []), time_value, camera, width, height)
    add_effects(primitives, data.get("effects", []), time_value, camera, width, height)

    raster = Raster(width, height)
    for primitive in sorted(primitives, key=lambda item: item.depth, reverse=True):
        if primitive.kind == "polygon":
            raster.polygon(primitive.points, primitive.color, primitive.outline)
        elif primitive.kind == "line":
            if primitive.outline and primitive.width > 2:
                raster.line(primitive.points[0], primitive.points[1], primitive.outline, primitive.width + 2)
            raster.line(primitive.points[0], primitive.points[1], primitive.color, primitive.width)
        elif primitive.kind == "disc":
            radius = int(primitive.points[1][0])
            raster.disc(primitive.points[0], radius, primitive.color, primitive.outline)

    raster.rect(0, 0, width, 30, (8, 10, 13))
    frame_time = f"{time_value:05.2f}/{data['shots'][-1]['end']:05.2f}S"
    label = f"{shot['id']} {shot.get('label', '')}  {camera.lens_mm:.0f}MM  {frame_time}"
    draw_text(raster, label[:70], 10, 7, 3, (230, 234, 239))
    return bytes(raster.buffer)


def find_ffmpeg(explicit: str | None) -> str | None:
    configured = explicit or os.environ.get("WHITEBOX_FFMPEG")
    if configured:
        candidate = Path(configured).expanduser()
        return str(candidate.resolve()) if candidate.is_file() else None
    return shutil.which("ffmpeg")


def probe(ffmpeg: str, output: Path, explicit_ffprobe: str | None = None) -> dict:
    sibling = Path(ffmpeg).with_name("ffprobe.exe" if Path(ffmpeg).suffix.lower() == ".exe" else "ffprobe")
    ffprobe = explicit_ffprobe or os.environ.get("WHITEBOX_FFPROBE") or shutil.which("ffprobe") or str(sibling)
    if not Path(ffprobe).exists():
        return {"probe": "ffprobe_not_found", "file_bytes": output.stat().st_size}
    command = [
        ffprobe, "-v", "error", "-show_entries", "format=duration,size", "-show_entries", "stream=codec_name,width,height,r_frame_rate,nb_frames",
        "-of", "json", str(output),
    ]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    if result.returncode != 0:
        return {"probe": "failed", "stderr": result.stderr.strip(), "file_bytes": output.stat().st_size}
    return json.loads(result.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validation-output", type=Path)
    parser.add_argument("--ffmpeg")
    parser.add_argument("--ffprobe")
    parser.add_argument("--crf", type=int, default=18)
    args = parser.parse_args()

    data = json.loads(args.spec.read_text(encoding="utf-8"))
    validation = validate(data)
    if not validation["ready"]:
        print(json.dumps(validation, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    ffmpeg = find_ffmpeg(args.ffmpeg)
    if not ffmpeg:
        print("ffmpeg was not found; pass --ffmpeg, set WHITEBOX_FFMPEG, or add ffmpeg to PATH", file=sys.stderr)
        return 3

    args.output.parent.mkdir(parents=True, exist_ok=True)
    width, height = data["resolution"]
    fps = data["fps"]
    duration = float(data["shots"][-1]["end"])
    frame_count = max(1, round(duration * fps))
    command = [
        ffmpeg, "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", str(args.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(args.output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame in range(frame_count):
            time_value = min(duration - 1e-7, frame / fps)
            process.stdin.write(render_frame(data, time_value))
    except BrokenPipeError:
        pass
    finally:
        process.stdin.close()
    stderr = process.stderr.read().decode("utf-8", errors="replace") if process.stderr else ""
    return_code = process.wait()
    if return_code != 0:
        print(stderr, file=sys.stderr)
        return 4

    validation.update(
        {
            "renderer": "whitebox-software-3d-v0.1",
            "ffmpeg": os.path.abspath(ffmpeg),
            "output": str(args.output.resolve()),
            "frame_count": frame_count,
            "expected_duration_seconds": duration,
            "shot_timing": [
                {
                    "id": shot["id"],
                    "start_seconds": shot["start"],
                    "end_seconds": shot["end"],
                    "start_frame": round(shot["start"] * fps),
                    "exclusive_end_frame": round(shot["end"] * fps),
                }
                for shot in data["shots"]
            ],
            "compile_notes": data.get("compile_notes", []),
            "media_probe": probe(ffmpeg, args.output, args.ffprobe),
            "output_sha256": hashlib.sha256(args.output.read_bytes()).hexdigest().upper(),
        }
    )
    validation_path = args.validation_output or args.output.with_name("previs_validation.json")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
