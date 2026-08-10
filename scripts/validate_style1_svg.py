#!/usr/bin/env python3
"""Validate the flat geometric and accent-count contract for Style-1 SVGs."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


FORBIDDEN_TAGS = {
    "linearGradient",
    "radialGradient",
    "filter",
    "image",
    "foreignObject",
    "pattern",
    "mask",
}
GEOMETRY_TAGS = {"rect", "circle", "ellipse", "polygon", "polyline", "path", "line"}
ALLOWED_PATH_COMMANDS = set("MmLlHhVvZz")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def shape_family(tag: str, attrs: dict[str, str]) -> str:
    if tag in {"circle", "ellipse"}:
        return "circle"
    if tag == "rect":
        return "rectangle"
    if tag in {"polygon", "polyline"}:
        point_count = len(attrs.get("points", "").strip().split())
        return "triangle" if point_count == 3 else "quadrilateral"
    if tag == "path":
        return "straight-path"
    return tag


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg", type=Path)
    parser.add_argument("--max-colors", type=int, default=8)
    parser.add_argument("--min-accents", type=int, default=1)
    parser.add_argument("--max-accents", type=int, default=5)
    parser.add_argument("--max-accent-families", type=int, default=2)
    parser.add_argument("--max-path-vertices", type=int, default=6)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    colors: set[str] = set()
    accent_count = 0
    base_count = 0
    accent_families: set[str] = set()

    try:
        root = ET.parse(args.svg).getroot()
    except (OSError, ET.ParseError) as exc:
        print(f"ERROR: cannot parse {args.svg}: {exc}", file=sys.stderr)
        return 2

    if local_name(root.tag) != "svg":
        errors.append("root element must be <svg>")

    for element in root.iter():
        tag = local_name(element.tag)
        attrs = {key.rsplit("}", 1)[-1]: value for key, value in element.attrib.items()}

        if tag in FORBIDDEN_TAGS:
            errors.append(f"forbidden element <{tag}>")
        if tag == "text":
            errors.append("visible <text> is forbidden")

        if tag in GEOMETRY_TAGS:
            role = attrs.get("data-role", "")
            if role == "accent":
                accent_count += 1
                accent_families.add(shape_family(tag, attrs))
            elif role == "base":
                base_count += 1
            else:
                errors.append(f"<{tag}> must declare data-role=\"base\" or data-role=\"accent\"")

        style_blob = " ".join(f"{key}:{value}" for key, value in attrs.items()).lower()
        if "url(" in style_blob:
            errors.append(f"<{tag}> uses a URL-based paint/filter")
        if "opacity" in style_blob:
            errors.append(f"<{tag}> uses opacity")
        if "filter" in attrs or "mask" in attrs:
            errors.append(f"<{tag}> uses a filter or mask")

        stroke = attrs.get("stroke", "").strip().lower()
        if stroke and stroke not in {"none", "transparent"}:
            errors.append(f"<{tag}> uses a visible stroke")

        fill = attrs.get("fill", "").strip().lower()
        if fill and fill not in {"none", "transparent", "currentcolor"} and not fill.startswith("url("):
            colors.add(fill)

        if tag == "path":
            data = attrs.get("d", "")
            commands = re.findall(r"[A-Za-z]", data)
            unsupported = sorted(set(commands) - ALLOWED_PATH_COMMANDS)
            if unsupported:
                errors.append(f"<path> uses non-linear or unsupported commands: {''.join(unsupported)}")
            vertices = sum(command in "MmLlHhVv" for command in commands)
            if vertices > args.max_path_vertices:
                errors.append(
                    f"<path> has {vertices} straight vertices; maximum is {args.max_path_vertices}"
                )

        if tag in {"polygon", "polyline"}:
            points = attrs.get("points", "").strip().split()
            if len(points) not in {3, 4}:
                errors.append(f"<{tag}> must use exactly 3 or 4 points")

    if base_count == 0:
        errors.append("SVG contains no data-role=\"base\" fields")
    if not args.min_accents <= accent_count <= args.max_accents:
        errors.append(
            f"accent count is {accent_count}; required range is {args.min_accents}-{args.max_accents}"
        )
    if len(accent_families) > args.max_accent_families:
        errors.append(
            f"uses {len(accent_families)} accent families; maximum is {args.max_accent_families}: "
            + ", ".join(sorted(accent_families))
        )
    if len(colors) > args.max_colors:
        errors.append(
            f"uses {len(colors)} colors; maximum is {args.max_colors}: {', '.join(sorted(colors))}"
        )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} issue(s)", file=sys.stderr)
        return 1

    print(f"OK: {args.svg}")
    print(
        f"base_shapes={base_count} accents={accent_count} "
        f"accent_families={len(accent_families)} colors={len(colors)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

