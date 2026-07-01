from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


NODES = (
    "Dataset Runner\n(not garak scheduler)",
    "Prompt Renderer\n[[TURN:*]]",
    "OpenAI-compatible\nGuard Proxy",
    "Groq / Mock Model",
    "P / I / O / F\nGuard Layer",
    "garak detectors",
    "stage5_pattern",
    "T1-T9 Taxonomy",
    "Metrics + Reports",
)


def render_architecture_figures(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    mermaid = """flowchart LR
  A["Dataset Runner<br/>(not garak scheduler)"] --> B["Prompt Renderer<br/>[[TURN:*]]"]
  B --> C["OpenAI-compatible Guard Proxy"]
  C --> D["Groq / Mock Model"]
  D --> E["P / I / O / F Guard Layer"]
  E --> G["garak detectors"]
  E --> H["stage5_pattern"]
  G --> I["T1-T9 Taxonomy"]
  H --> I
  I --> J["Metrics + Reports"]
"""
    (directory / "stage5_architecture.mmd").write_text(mermaid, encoding="utf-8")

    width, height = 3200, 1800
    positions = [
        (120, 690), (470, 690), (830, 690), (1200, 690), (1540, 690),
        (1940, 480), (1940, 900), (2350, 690), (2760, 690),
    ]
    box_w, box_h = 300, 210
    colors = ["#E8F1FA", "#F4F7F9", "#DDEFE8", "#F8E9D2", "#EADFF2",
              "#D8EAF8", "#F5E3E7", "#E4EED8", "#E8E8E8"]
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#333"/></marker></defs>',
        '<rect width="100%" height="100%" fill="white"/>',
    ]
    edges = [(0,1),(1,2),(2,3),(3,4),(4,5),(4,6),(5,7),(6,7),(7,8)]
    for source, target in edges:
        sx, sy = positions[source]
        tx, ty = positions[target]
        svg.append(
            f'<line x1="{sx+box_w}" y1="{sy+box_h/2}" x2="{tx}" y2="{ty+box_h/2}" stroke="#333" stroke-width="5" marker-end="url(#arrow)"/>'
        )
    for index, (label, (x, y)) in enumerate(zip(NODES, positions)):
        svg.append(
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="12" fill="{colors[index]}" stroke="#333" stroke-width="4"/>'
        )
        lines = label.split("\n")
        for offset, line in enumerate(lines):
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg.append(
                f'<text x="{x+box_w/2}" y="{y+90+offset*48}" text-anchor="middle" font-family="Arial" font-size="28">{escaped}</text>'
            )
    svg.append("</svg>")
    (directory / "stage5_architecture.svg").write_text(
        "\n".join(svg), encoding="utf-8"
    )

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default(size=34)
    for source, target in edges:
        sx, sy = positions[source]
        tx, ty = positions[target]
        draw.line((sx + box_w, sy + box_h // 2, tx, ty + box_h // 2), fill="#333333", width=6)
    for index, (label, (x, y)) in enumerate(zip(NODES, positions)):
        draw.rounded_rectangle(
            (x, y, x + box_w, y + box_h),
            radius=12,
            fill=colors[index],
            outline="#333333",
            width=4,
        )
        draw.multiline_text(
            (x + box_w // 2, y + box_h // 2),
            label,
            fill="#111111",
            font=font,
            anchor="mm",
            align="center",
            spacing=10,
        )
    image.save(directory / "stage5_architecture.png")
