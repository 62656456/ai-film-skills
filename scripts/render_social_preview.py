#!/usr/bin/env python3
"""Render a new Open Film Skills preview using pinned font inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "assets" / "social-preview.png"
PINNED_FONT_DIR = ROOT / "docs" / "assets" / "fonts"

COLORS = {
    "slate": "#0B0F14",
    "grid": "#1F2935",
    "paper": "#F4F0E8",
    "muted": "#AAB4C0",
    "dim": "#6F7C8C",
    "orange": "#FF6B35",
    "cyan": "#46C2CB",
    "brass": "#D6A756",
    "blue": "#5B8CFF",
    "green": "#7EE2A8",
}


def font_dir_default() -> Path:
    configured = os.environ.get("OPEN_FILM_SKILLS_FONT_DIR")
    if configured:
        return Path(configured)
    return PINNED_FONT_DIR


def font(size: int, bold: bool = False, font_dir: Path | None = None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    candidate = (font_dir or PINNED_FONT_DIR) / name
    expected = json.loads((PINNED_FONT_DIR / "manifest.json").read_text(encoding="utf-8"))["files"][name]
    if hashlib.sha256(candidate.read_bytes()).hexdigest() != expected:
        raise ValueError(f"Font must match the pinned DejaVu Sans 2.37 input: {name}")
    return ImageFont.truetype(str(candidate), size)


def render(output: Path, font_dir: Path | None) -> None:
    image = Image.new("RGB", (1280, 640), COLORS["slate"])
    draw = ImageDraw.Draw(image)

    for y in (106, 212, 318, 424, 530):
        draw.line((0, y, 1280, y), fill=COLORS["grid"], width=1)
    for x in (128, 320, 512, 704, 896, 1088):
        draw.line((x, 0, x, 640), fill=COLORS["grid"], width=1)

    draw.rounded_rectangle((64, 52, 316, 86), radius=17, fill=COLORS["orange"])
    label = "OPEN-SOURCE AGENT SKILLS"
    label_box = draw.textbbox((0, 0), label, font=font(14, True, font_dir))
    draw.text((190 - (label_box[2] - label_box[0]) / 2, 60), label, fill=COLORS["slate"], font=font(14, True, font_dir))

    draw.text((64, 112), "OPEN FILM SKILLS", fill=COLORS["paper"], font=font(68, True, font_dir))
    draw.text((66, 205), "Script -> assets -> cinematic storyboard -> AI-video workflow", fill=COLORS["muted"], font=font(24, False, font_dir))
    draw.text((66, 252), "19 standalone Skills  |  Codex  |  Claude Code  |  TRAE  |  CodeBuddy  |  WorkBuddy", fill=COLORS["dim"], font=font(16, False, font_dir))

    draw.line((92, 436, 1188, 436), fill="#455260", width=4)
    nodes = [
        (104, COLORS["orange"], "WRITE"),
        (326, COLORS["cyan"], "ASSETS"),
        (548, COLORS["brass"], "DIRECT"),
        (770, COLORS["paper"], "PROMPT"),
        (992, COLORS["blue"], "PRODUCE"),
        (1176, COLORS["green"], "VERIFY"),
    ]
    for x, color, label in nodes:
        draw.ellipse((x - 17, 419, x + 17, 453), fill=color)
        draw.ellipse((x - 5, 431, x + 5, 441), fill=COLORS["slate"])
        box = draw.textbbox((0, 0), label, font=font(15, True, font_dir))
        draw.text((x - (box[2] - box[0]) / 2, 486), label, fill=COLORS["paper"], font=font(15, True, font_dir))

    draw.text((64, 570), "github.com/62656456/ai-film-skills", fill="#7F8C9B", font=font(15, False, font_dir))
    footer = "APACHE-2.0  |  v1.3.0"
    footer_box = draw.textbbox((0, 0), footer, font=font(14, False, font_dir))
    draw.text((1216 - (footer_box[2] - footer_box[0]), 570), footer, fill="#7F8C9B", font=font(14, False, font_dir))

    output.parent.mkdir(parents=True, exist_ok=True)
    image.save(output, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--font-dir", type=Path, default=font_dir_default())
    args = parser.parse_args()
    render(args.output.resolve(), args.font_dir.resolve() if args.font_dir else None)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
