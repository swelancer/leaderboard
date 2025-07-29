#!/usr/bin/env python3
"""
Build docs/index.html from data/results.csv.

* sorts by Earned descending
* inserts a Rank column
* renders templates/leaderboard.html.j2 via Jinja2
"""

import datetime as _dt
import pathlib as _p
import pandas as _pd
import jinja2 as _jinja


# ——————————————————— configuration ———————————————————
ROOT        = _p.Path(__file__).resolve().parent.parent
CSV_PATH    = ROOT / "data" / "results.csv"
HTML_OUT    = ROOT / "docs" / "index.html"
TEMPLATE    = ROOT / "templates" / "leaderboard.html.j2"
METRIC_COL  = "Earned"      # column that decides ranking
# ————————————————————————————————————————————————————————


def _load_data():
    df = _pd.read_csv(CSV_PATH)

    # make sure metric column is numeric
    df[METRIC_COL] = _pd.to_numeric(df[METRIC_COL], errors="coerce")

    # order: best → worst
    df = df.sort_values(METRIC_COL, ascending=False).reset_index(drop=True)

    # rank is 1-based
    df.insert(0, "Rank", df.index + 1)

    # prettier date column if present
    if "Date" in df.columns:
        df["Date"] = _pd.to_datetime(df["Date"], errors="coerce").dt.date

    return df


def _render(df):
    env = _jinja.Environment(
        loader=_jinja.FileSystemLoader(TEMPLATE.parent),
        autoescape=True,
    )
    html = env.get_template(TEMPLATE.name).render(
        rows=df.to_dict(orient="records"),
        generated=_dt.date.today().isoformat(),
        description=(
            "Follow the <a href='https://github.com/swelancer/leaderboard/blob/main/README.md' target='_blank' style='color: var(--primary-color); text-decoration: none; font-weight: 600; border-bottom: 1px solid var(--primary-color); transition: all 0.2s ease;' onmouseover='this.style.color=\"var(--accent-color)\"; this.style.borderBottomColor=\"var(--accent-color)\"' onmouseout='this.style.color=\"var(--primary-color)\"; this.style.borderBottomColor=\"var(--primary-color)\"'>README</a> instructions for how to add a folder to submissions. We will verify your submission and update the leaderboard."
            "\nImportant note: the leaderboard only contains tasks from the 198 diamond offline subset."
        ),
    )
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"✓ wrote {HTML_OUT.relative_to(ROOT)}")


def main():
    df = _load_data()
    _render(df)


if __name__ == "__main__":
    main()
