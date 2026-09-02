# Design Principles for Fluctuation-Responsive Station Areas

Interactive gallery of design principles from thesis research on demand-responsive station areas.

## Live deployments

| Version | Platform | URL |
|---------|----------|-----|
| **Static** (always on) | GitHub Pages | https://1309928130.github.io/design-principles/ |
| **Dynamic** (Flask) | Render | https://design-principles.onrender.com/ |

## Repository structure

```
5_design_principles/
  app_2.py                 # Flask app (dynamic version)
  design_principles_coding.csv
  static/image/            # Principle images (~150 MB)
  templates/                 # Jinja templates
  scripts/build_static.py    # Builds GitHub Pages site into docs/
  docs/                      # Static site output (GitHub Pages)
  render.yaml                # Render deployment config
  requirements.txt
```

## Local development (dynamic Flask)

```bash
pip install -r requirements.txt
python app_2.py
```

Open http://localhost:5000

## Build static site (GitHub Pages)

```bash
python scripts/build_static.py
```

This generates `docs/` with pre-built HTML pages and copies all static assets.

### Enable GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Source: **Deploy from branch**
4. Branch: `main`, folder: `/docs`
5. Save — site will be at `https://1309928130.github.io/design-principles/`

## Deploy dynamic version on Render

1. Push repo to GitHub
2. Go to [render.com](https://render.com) → **New → Blueprint**
3. Connect `1309928130/design-principles`
4. Render reads `render.yaml` automatically
5. Deploy — free tier sleeps after 15 min idle, wakes on next visit (~1 min)

Or manually: **New Web Service** → connect repo → Build: `pip install -r requirements.txt` → Start: `gunicorn app_2:app`

## Features

- Browse 25 design principles with thumbnail gallery
- Filter by perspective (paradigm, spatial/managerial, indoor/outdoor, etc.)
- Detail pages with image galleries and descriptions
- Event typology and network pattern views
- Disqus comments (dynamic version)

## Data

- `design_principles_coding.csv` — main dataset (semicolon-delimited)
- `static/image/{N}/description.csv` — per-principle image descriptions

## License

Thesis research project — TU Delft.
