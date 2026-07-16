#!/usr/bin/env python3
"""Regenerate the dark/light GitHub terminal profile cards.

The card uses a photo-derived ASCII portrait stored in
``assets/profile_ascii.txt`` and a single SMIL-powered blinking cursor.
The output is self-contained and compatible with GitHub profile READMEs.

Design concept adapted from the ASCII Terminal Art guide by Careers with Aniket.
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

INFO = [
    ("Role", "AI Transformation & Technical Project Management"),
    ("Focus", "Cloud Delivery | AIOps | PMO | ITSM/ITOM"),
    ("Experience", "SAP Cloud PMO + IBM/Kyndryl IT Operations"),
    ("Education", "RWTH Aachen M.Sc. Management & Engineering"),
    ("Code", "Python | SQL | Pandas | scikit-learn"),
    ("Build", "Streamlit | Plotly | GitHub Actions | Docker"),
    ("Methods", "RAID | RACI | ITIL | Stakeholder Management"),
    ("Projects", "5 live recruiter-demo applications"),
    ("Quality", "Automated tests | CI | synthetic data"),
    ("Languages", "English | German A2 | Hindi | Bengali | Marathi"),
    ("Location", "Germany | Germany-wide opportunities"),
    ("Status", "Open to junior / associate technology roles"),
]

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "panel": "#161b22",
        "border": "#30363d",
        "text": "#c9d1d9",
        "muted": "#8b949e",
        "key": "#ffa657",
        "value": "#79c0ff",
        "green": "#3fb950",
        "accent": "#d2a8ff",
        "portrait": "#d8dee9",
    },
    "light": {
        "bg": "#ffffff",
        "panel": "#f6f8fa",
        "border": "#d0d7de",
        "text": "#24292f",
        "muted": "#57606a",
        "key": "#953800",
        "value": "#0969da",
        "green": "#1a7f37",
        "accent": "#8250df",
        "portrait": "#24292f",
    },
}


def load_portrait(root: Path) -> list[str]:
    portrait_path = root / "assets" / "profile_ascii.txt"
    rows = portrait_path.read_text(encoding="utf-8").splitlines()
    if not rows:
        raise ValueError("assets/profile_ascii.txt is empty")
    return rows


def build_svg(theme_name: str, portrait_rows: list[str]) -> str:
    theme = THEMES[theme_name]
    width, height = 1200, 650

    parts = [
        (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' "
            f"height='{height}' viewBox='0 0 {width} {height}' role='img' "
            "aria-labelledby='title desc'>"
        ),
        "<title id='title'>Samadrita Acharya terminal-style GitHub profile card</title>",
        (
            "<desc id='desc'>Photo-derived ASCII portrait of Samadrita Acharya "
            "beside a professional profile summary for AI transformation, "
            "technical project management, cloud delivery, AIOps, PMO and ITSM.</desc>"
        ),
        f"<rect width='{width}' height='{height}' rx='24' fill='{theme['bg']}'/>",
        (
            f"<rect x='12' y='12' width='{width - 24}' height='{height - 24}' "
            f"rx='18' fill='{theme['panel']}' stroke='{theme['border']}' "
            "stroke-width='2'/>"
        ),
        (
            "<circle cx='40' cy='38' r='7' fill='#ff5f56'/>"
            "<circle cx='64' cy='38' r='7' fill='#ffbd2e'/>"
            "<circle cx='88' cy='38' r='7' fill='#27c93f'/>"
        ),
        (
            f"<text x='112' y='44' fill='{theme['muted']}' "
            "font-family='Consolas, Menlo, monospace' font-size='16'>"
            "profile.sh - samadrita@github</text>"
        ),
        (
            f"<line x1='28' y1='62' x2='{width - 28}' y2='62' "
            f"stroke='{theme['border']}'/>"
        ),
        (
            "<style>"
            "text{font-family:Consolas,Menlo,'DejaVu Sans Mono',monospace;"
            "white-space:pre}"
            f".portrait{{fill:{theme['portrait']}}}"
            f".muted{{fill:{theme['muted']}}}"
            f".key{{fill:{theme['key']};font-weight:700}}"
            f".value{{fill:{theme['value']}}}"
            f".accent{{fill:{theme['accent']}}}"
            "</style>"
        ),
    ]

    portrait_x = 60
    portrait_y = 88
    line_height = 13.35
    for index, row in enumerate(portrait_rows):
        y = portrait_y + index * line_height
        parts.append(
            f"<text class='portrait' x='{portrait_x}' y='{y:.2f}' "
            f"font-size='13.0'>{escape(row)}</text>"
        )

    parts.extend(
        [
            (
                "<text x='72' y='607' class='accent' font-size='16'>"
                "AI Transformation + Technical Delivery</text>"
            ),
            (
                "<text x='72' y='630' class='muted' font-size='13'>"
                "Photo-derived ASCII | live apps | tested workflows</text>"
            ),
            (
                f"<line x1='465' y1='82' x2='465' y2='620' "
                f"stroke='{theme['border']}' stroke-width='2'/>"
            ),
            (
                f"<text x='505' y='101' fill='{theme['green']}' "
                "font-size='20' font-weight='700'>samadrita@github</text>"
            ),
            (
                "<text x='505' y='128' class='muted' font-size='14'>"
                "--------------- professional profile ---------------</text>"
            ),
        ]
    )

    y = 160
    for key, value in INFO:
        prefix = f". {key}:"
        dots = "." * max(3, 60 - len(prefix) - len(value))
        parts.append(
            f"<text x='505' y='{y}' font-size='14'>"
            "<tspan class='muted'>. </tspan>"
            f"<tspan class='key'>{escape(key)}</tspan>"
            f"<tspan class='muted'>: {dots} </tspan>"
            f"<tspan class='value'>{escape(value)}</tspan></text>"
        )
        y += 31

    prompt_y = 605
    parts.extend(
        [
            (
                f"<text x='505' y='{prompt_y}' fill='{theme['green']}' "
                "font-size='16'>samadrita@github</text>"
            ),
            (
                f"<text x='665' y='{prompt_y}' fill='{theme['text']}' "
                "font-size='16'>:~$</text>"
            ),
            (
                f"<rect x='706' y='{prompt_y - 15}' width='10' height='18' "
                f"fill='{theme['green']}'>"
                "<animate attributeName='opacity' values='1;1;0;0' "
                "keyTimes='0;0.5;0.5;1' dur='1.1s' "
                "repeatCount='indefinite'/></rect>"
            ),
            "</svg>",
        ]
    )
    return "\n".join(parts)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    portrait_rows = load_portrait(root)
    for theme_name in THEMES:
        output = root / f"{theme_name}_mode.svg"
        output.write_text(
            build_svg(theme_name, portrait_rows),
            encoding="utf-8",
        )
        print(f"Wrote {output.relative_to(root)}")


if __name__ == "__main__":
    main()
