#!/usr/bin/env python3
"""Build static site into docs/ for GitHub Pages."""

from __future__ import annotations

import csv
import json
import re
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
STATIC_SRC = ROOT / "static"
CSV_PATH = ROOT / "design_principles_coding.csv"
EVENT_TYPOLOGY = ROOT / "templates" / "event_typology.html"

SKIP_COLS = {
    "real index",
    "index",
    "picture_location",
    "design_principle_name",
    "detail_pictures_folder",
}


def load_principles() -> list[dict]:
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter=";"))
    for index, row in enumerate(rows):
        row["_idx"] = index
    return rows


def load_image_descriptions(folder: str) -> dict[str, str]:
    csv_path = STATIC_SRC / "image" / folder / "description.csv"
    if not csv_path.exists():
        return {}
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return {
            row["filename"]: row["description"]
            for row in csv.DictReader(handle)
            if row.get("filename") and not row["filename"].startswith(".DS_Store")
        }


def dimension_columns(rows: list[dict]) -> list[str]:
    return [col for col in rows[0].keys() if col not in SKIP_COLS and col != "_idx"]


def paragraphs_html(text: str) -> str:
    return "\n".join(
        f"<p>{escape(part.strip())}</p>"
        for part in (text or "").split("\n")
        if part.strip()
    )


def render_detail_page(row: dict) -> str:
    descriptions = load_image_descriptions(row["detail_pictures_folder"])
    gallery = []
    for filename, description in descriptions.items():
        gallery.append(
            f"""
            <div class="image-container">
              <div class="image-wrapper">
                <img src="../static/image/{escape(row['detail_pictures_folder'])}/{escape(filename)}"
                     alt="Detail Picture" class="detail-image">
              </div>
              <div class="description">{paragraphs_html(description)}</div>
            </div>
            """
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="../static/image/dp_logo.png" type="image/png">
  <title>{escape(row['design_principle_name'])}</title>
  <style>
    body {{
      font-family: "Roboto", sans-serif;
      font-weight: 400;
      font-size: 20px;
      color: black;
      margin: 0;
      text-align: center;
    }}
    .image-container, .main-image, .background_description {{
      width: 100%;
      box-sizing: border-box;
      margin-bottom: 40px;
    }}
    .image-wrapper {{ position: relative; }}
    .description, .background_description {{
      background-color: rgba(255, 255, 255, 0.8);
      padding: 10px;
      text-align: left;
      margin-top: 10px;
    }}
    .main-image {{ width: 100%; height: auto; margin: 10px 0; }}
    .detail-image {{ width: 100%; height: auto; }}
    @media (min-width: 768px) {{
      .image-container, .main-image, .background_description {{
        width: 60%;
        margin-left: auto;
        margin-right: auto;
      }}
    }}
    .back-link {{
      display: inline-block;
      margin: 20px 0;
      color: #333;
      text-decoration: none;
      font-size: 16px;
    }}
  </style>
</head>
<body>
  <a class="back-link" href="../index.html">← Back to all principles</a>
  <h1>{escape(row['design_principle_name'])}</h1>
  <img src="../static/{escape(row['picture_location'])}" alt="Picture" class="main-image">
  <div class="image-gallery">{''.join(gallery)}</div>
  <p class="background_description">Source of heuristics: <strong>{escape(row['Source of heuristics'])}</strong></p>
</body>
</html>
"""


def render_index_page(rows: list[dict], dimensions: list[str]) -> str:
  # Build JSON payload for client-side filtering
    payload = {
        "principles": rows,
        "dimensions": dimensions,
    }
    data_json = json.dumps(payload, ensure_ascii=False)
    event_html = EVENT_TYPOLOGY.read_text(encoding="utf-8") if EVENT_TYPOLOGY.exists() else ""

    dimension_options = "\n".join(
        f'<option value="{escape(col)}">{escape(col)}</option>' for col in dimensions
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" href="static/image/dp_logo.png" type="image/png">
  <title>Design Principles</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;400;1000&display=swap" rel="stylesheet">
  <style>
    body {{ margin: 0; }}
    .main-heading {{
      text-align: center;
      font-family: "Roboto", sans-serif;
      font-weight: 100;
      font-size: 50px;
      color: black;
      margin: 10px 0;
    }}
    .dropdown-container {{
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
      gap: 8px;
    }}
    .dropdown-label {{
      font-family: "Roboto", sans-serif;
      font-size: 25px;
    }}
    .dropdown-menu {{
      border: 1px solid #000;
      border-radius: 25px;
      font-family: "Roboto", sans-serif;
      font-size: 25px;
      font-weight: 1000;
      text-align: center;
      padding: 4px 12px;
    }}
    .principles-container {{
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-start;
      margin-left: 30px;
    }}
    .principles-row {{ display: flex; flex-wrap: wrap; }}
    .principle {{
      position: relative;
      cursor: pointer;
      z-index: 1;
      margin: 5px;
    }}
    .principle img {{
      width: 210px;
      height: 140px;
      object-fit: cover;
      transition: transform 0.3s ease-in-out;
    }}
    .principle:hover {{ z-index: 2; }}
    .principle:hover img {{ transform: scale(1.5); z-index: 3; }}
    .tooltip {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      visibility: hidden;
      width: 500px;
      color: black;
      font-family: "Roboto", sans-serif;
      font-size: 20px;
      font-weight: 1000;
      text-align: center;
      text-shadow: -1px -1px 0 white, 1px -1px 0 white, -1px 1px 0 white, 1px 1px 0 white;
      z-index: 3;
    }}
    .principle:hover .tooltip {{ visibility: visible; }}
    .row-container {{ display: block; flex-basis: 100%; }}
    .row-title {{
      display: block;
      flex-basis: 100%;
      margin-top: 20px;
      font-family: "Roboto", sans-serif;
      font-weight: 1000;
      font-size: 25px;
    }}
    .index-number {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 1;
      background-color: rgba(255, 255, 255, 0.7);
      width: 60px;
      height: 60px;
      border-radius: 50%;
      font-family: "Roboto", sans-serif;
      font-size: 50px;
      font-weight: 100;
      text-align: center;
      line-height: 60px;
      color: black;
    }}
    .principle:hover .index-number {{ opacity: 0; }}
    .special-content img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}
    .special-content {{ padding: 0 20px 40px; }}
  </style>
</head>
<body>
  <h1 class="main-heading">Design Principles for Fluctuation-Responsive Station Areas</h1>
  <div class="dropdown-container">
    <span class="dropdown-label">Perspective ➭</span>
    <select id="dimensionSelect" class="dropdown-menu">
      <option value="">All</option>
      <option value="Patterns in a Network">Patterns in a Network</option>
      <option value="Related to an Event Typology">Related to an Event Typology</option>
      {dimension_options}
    </select>
  </div>
  <div class="principles-container" id="principles-container"></div>

  <template id="event-typology-template">{event_html}</template>

  <script id="principles-data" type="application/json">{data_json}</script>
  <script>
    const {{ principles, dimensions }} = JSON.parse(document.getElementById('principles-data').textContent);

    function principleCard(row) {{
      const idx = row._idx;
      return `
        <div class="principle">
          <a href="detail/${{idx}}.html" target="_blank">
            <span class="index-number">${{row.index}}</span>
            <img src="static/${{row.picture_location}}" alt="Picture">
            <div class="tooltip"><p>${{row.design_principle_name}}</p></div>
          </a>
        </div>`;
    }}

    function renderAll() {{
      const container = document.getElementById('principles-container');
      container.innerHTML = principles.map(principleCard).join('');
    }}

    function renderGrouped(dimension) {{
      const container = document.getElementById('principles-container');
      const groups = new Map();
      principles.forEach((row) => {{
        const key = row[dimension] || '(empty)';
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(row);
      }});
      container.innerHTML = [...groups.entries()].map(([title, rows]) => `
        <div class="row-container">
          <div class="row-title">${{title}}</div>
          <div class="principles-row">${{rows.map(principleCard).join('')}}</div>
        </div>
      `).join('');
    }}

    function renderThemes() {{
      const container = document.getElementById('principles-container');
      const themes = new Set();
      principles.forEach((row) => {{
        (row['(Other) Themes'] || '').split('/').forEach((theme) => {{
          const trimmed = theme.trim();
          if (trimmed) themes.add(trimmed);
        }});
      }});
      const html = [...themes].sort().map((theme) => {{
        const rows = principles.filter((row) => (row['(Other) Themes'] || '').includes(theme));
        return `
          <div class="row-container">
            <div class="row-title">${{theme}}</div>
            <div class="principles-row">${{rows.map(principleCard).join('')}}</div>
          </div>`;
      }}).join('');
      container.innerHTML = html;
    }}

    function renderPatterns() {{
      document.getElementById('principles-container').innerHTML = `
        <div class="special-content">
          <img src="static/Pattern_Network_8M.png" alt="Patterns in a Network">
        </div>`;
    }}

    function renderEventTypology() {{
      const template = document.getElementById('event-typology-template');
      document.getElementById('principles-container').innerHTML = `
        <div class="special-content">
          <img src="static/event_principles.png" alt="Event Principles Image">
          ${{template.innerHTML}}
        </div>`;
    }}

    function renderDimension(value) {{
      if (!value || value === 'All') return renderAll();
      if (value === 'Patterns in a Network') return renderPatterns();
      if (value === 'Related to an Event Typology') return renderEventTypology();
      if (value === '(Other) Themes') return renderThemes();
      return renderGrouped(value);
    }}

    document.getElementById('dimensionSelect').addEventListener('change', (event) => {{
      renderDimension(event.target.value);
    }});

    const params = new URLSearchParams(window.location.search);
    const selected = params.get('dimension') || '';
    if (selected) {{
      document.getElementById('dimensionSelect').value = selected;
    }}
    renderDimension(selected);
  </script>
</body>
</html>
"""


def copy_static_assets() -> None:
    target = DOCS / "static"
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(STATIC_SRC, target)


def main() -> None:
    rows = load_principles()
    dimensions = dimension_columns(rows)

    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    (DOCS / "detail").mkdir()
    (DOCS / ".nojekyll").touch()

    (DOCS / "index.html").write_text(render_index_page(rows, dimensions), encoding="utf-8")
    for row in rows:
        detail_path = DOCS / "detail" / f"{row['_idx']}.html"
        detail_path.write_text(render_detail_page(row), encoding="utf-8")

    copy_static_assets()
    print(f"Built static site in {DOCS} ({len(rows)} detail pages)")


if __name__ == "__main__":
    main()
