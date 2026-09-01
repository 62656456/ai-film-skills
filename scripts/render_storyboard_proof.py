#!/usr/bin/env python3
"""Render the Storyboard Director 5.4.4 before/after proof as PNG."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from render_social_preview import COLORS, font, font_dir_default


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "assets" / "storyboard-544-proof.png"


def render(output: Path, font_dir: Path | None) -> None:
    image = Image.new("RGB", (1200, 560), COLORS["slate"])
    draw = ImageDraw.Draw(image)
    for y in (80, 160, 240, 320, 400, 480):
        draw.line((0, y, 1200, y), fill=COLORS["grid"], width=1)
    for x in (120, 300, 480, 660, 840, 1020):
        draw.line((x, 0, x, 560), fill=COLORS["grid"], width=1)

    draw.rounded_rectangle((52, 38, 254, 68), radius=15, fill=COLORS["orange"])
    draw.text((72, 44), "STORYBOARD 5.4.4", fill=COLORS["slate"], font=font(13, True, font_dir))
    draw.text((52, 84), "See the camera plan before generation.", fill=COLORS["paper"], font=font(40, True, font_dir))
    draw.text((54, 142), "A heading should tell a human how the shot is staged - not only what happens.", fill=COLORS["muted"], font=font(17, False, font_dir))

    draw.rounded_rectangle((52, 198, 428, 474), radius=8, fill="#121923", outline="#394552", width=2)
    draw.text((78, 222), "STORY-ONLY HEADING", fill="#7F8C9B", font=font(12, True, font_dir))
    draw.text((78, 270), "[2.20-4.50s]", fill=COLORS["paper"], font=font(28, True, font_dir))
    draw.text((78, 320), "The gear slips.", fill=COLORS["paper"], font=font(23, False, font_dir))
    draw.line((78, 370, 400, 370), fill="#2B3541", width=2)
    draw.text((78, 394), "Lens?   Position?   Focus?", fill="#7F8C9B", font=font(15, False, font_dir))
    draw.text((78, 438), "The event is named. The shot is not.", fill="#FF8B64", font=font(14, True, font_dir))

    draw.line((458, 336, 520, 336), fill=COLORS["orange"], width=4)
    draw.line((509, 324, 526, 336), fill=COLORS["orange"], width=4)
    draw.line((509, 348, 526, 336), fill=COLORS["orange"], width=4)

    draw.rounded_rectangle((552, 198, 1148, 474), radius=8, fill="#121923", outline=COLORS["cyan"], width=2)
    draw.text((578, 222), "VISIBLE CAMERA CONTRACT", fill=COLORS["cyan"], font=font(12, True, font_dir))
    lines = [
        (270, "2.20-4.50s  |  50mm hand close-up", COLORS["paper"], True),
        (306, "Southeast of bench  |  15-degree high angle", COLORS["paper"], False),
        (342, "Locked camera  |  faces northwest  |  no movement", COLORS["paper"], False),
        (378, "Focus locked: fall path -> receiving palm", COLORS["paper"], False),
        (414, "Endpoint: falling gear makes physical contact with hand", COLORS["brass"], True),
        (450, "7 visible fields  |  fixed position  |  explicit focus", COLORS["green"], True),
    ]
    for y, value, color, bold in lines:
        draw.text((578, y), value, fill=color, font=font(16 if y != 450 else 14, bold, font_dir))

    draw.text((52, 522), "Verified text behavior  |  continuous 0.00-8.00s  |  no claim of video-model or user visual approval", fill=COLORS["dim"], font=font(13, False, font_dir))
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
