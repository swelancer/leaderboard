#!/usr/bin/env python3
"""
Generate docs/index.html from data/results.csv (GitHub-Pages leaderboard).

CSV schema (example):
Model,Earned (offline pass@1),Accuracy (offline pass@1),Submitter,Date
4o,0.08081,11500,OpenAI,2025-07-17
o1,0.27778,43625,OpenAI,2025-07-17
"""

import pathlib, datetime, pandas as pd, jinja2, textwrap

ROOT       = pathlib.Path(__file__).resolve().parents[1]
CSV_PATH   = ROOT / "data" / "results.csv"
HTML_PATH  = ROOT / "docs" / "index.html"

# Which metric decides the ranking?
METRIC_COL = "Earned (offline pass@1)"

# ------------------------------------------------------------------ load data
df = pd.read_csv(CSV_PATH)

# Make sure the metric column is numeric (strip commas etc. if needed)
df[METRIC_COL] = pd.to_numeric(df[METRIC_COL], errors="coerce")

# Rank: 1 = best (highest Earned)
df = df.sort_values(METRIC_COL, ascending=False).reset_index(drop=True)
df.insert(0, "Rank", df.index + 1)

# Pretty-print dates if present
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

# ---------------------------------------------------------------- render HTML
env  = jinja2.Environment(
        loader=jinja2.FileSystemLoader(ROOT / "templates"), autoescape=True)
html = env.get_template("leaderboard.html.j2").render(
        rows=df.to_dict(orient="records"),
        generated=datetime.date.today().isoformat(),
        description=textwrap.dedent("""
            Read the README for info on how to submit. After adding the correct folder to `submissions`, open a PR, and CI will rebuild this page automatically.
        """))

HTML_PATH.write_text(html, encoding="utf-8")
print(f"✓ Wrote {HTML_PATH.relative_to(ROOT)}")
