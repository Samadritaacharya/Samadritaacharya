#!/usr/bin/env python3
"""Convert a portrait photo into the ASCII source used by the profile card.

This utility uses Pillow only. It removes an edge-connected red studio
background, applies a recruiter-profile crop, enhances facial contrast, and
writes ``assets/profile_ascii.txt``.

Usage:
    python -m pip install Pillow
    python scripts/photo_to_ascii.py path/to/portrait.png

Optional:
    python scripts/photo_to_ascii.py portrait.png --width 48
"""
from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

RAMP = " .:-=+*#%@"


def is_red_background(pixel: tuple[int, int, int]) -> bool:
    """Return True for the saturated red studio background.

    The ratio is deliberately strict so warm skin, brown hair, and red lipstick
    are not removed. Only pixels connected to the outer image edge are treated
    as background.
    """
    red, green, blue = pixel
    return (
        red > 45
        and red > 3.0 * max(green, 1)
        and red > 1.8 * max(blue, 1)
    )


def remove_edge_background(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def push(x: int, y: int) -> None:
        index = y * width + x
        if visited[index] or not is_red_background(pixels[x, y]):
            return
        visited[index] = 1
        queue.append((x, y))

    for x in range(width):
        push(x, 0)
        push(x, height - 1)
    for y in range(height):
        push(0, y)
        push(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x > 0:
            push(x - 1, y)
        if x + 1 < width:
            push(x + 1, y)
        if y > 0:
            push(x, y - 1)
        if y + 1 < height:
            push(x, y + 1)

    output = rgb.copy()
    out = output.load()
    for y in range(height):
        offset = y * width
        for x in range(width):
            if visited[offset + x]:
                out[x, y] = (255, 255, 255)
    return output


def portrait_crop(image: Image.Image) -> Image.Image:
    """Crop tightly from above the hair to the upper torso."""
    width, height = image.size
    box = (
        int(width * 0.205),
        int(height * 0.078),
        int(width * 0.820),
        int(height * 0.663),
    )
    return image.crop(box)


def image_to_ascii(image: Image.Image, columns: int = 48) -> list[str]:
    gray = image.convert("L")
    gray = gray.point(lambda value: int(((value / 255.0) ** 0.78) * 255))
    gray = ImageOps.autocontrast(gray, cutoff=1)
    gray = ImageEnhance.Contrast(gray).enhance(1.35)
    gray = gray.filter(
        ImageFilter.UnsharpMask(radius=1, percent=130, threshold=3)
    )

    char_aspect = 0.68
    rows = max(
        1,
        int(columns * (gray.height / gray.width) * char_aspect),
    )
    resized = gray.resize((columns, rows), Image.Resampling.LANCZOS)
    pixels = resized.load()
    max_index = len(RAMP) - 1

    output: list[str] = []
    for y in range(rows):
        row = []
        for x in range(columns):
            luminance = pixels[x, y]
            index = int((255 - luminance) / 255 * max_index)
            row.append(RAMP[index])
        output.append("".join(row).rstrip())
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--width", type=int, default=48)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/profile_ascii.txt"),
    )
    args = parser.parse_args()

    image = Image.open(args.image)
    cleaned = remove_edge_background(image)
    cropped = portrait_crop(cleaned)
    rows = image_to_ascii(cropped, columns=args.width)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(
        f"Wrote {args.output} "
        f"({len(rows)} rows, max {max(map(len, rows))} columns)"
    )


if __name__ == "__main__":
    main()
