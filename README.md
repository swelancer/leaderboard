# SWE‑Lancer Leaderboard

This repository contains **(a)** the SWE‑Lancer benchmark data, **(b)** an automated grading workflow, and **(c)** the public leaderboard served via GitHub Pages.

---

## 1  Repository layout

```
<repo‑root>/
├── data/                  # Ground‑truth data & aggregated results
│   └── results.csv        # ← auto‑generated; DO NOT EDIT BY HAND
├── submissions/           # Community submissions land here (see §2)
│   └── <DisplayName>/     # one folder per submission, name = what shows on LB
│       └── <task‑id>/     # one folder per task, e.g. 25570_1192
│           └── patch.diff # model‑generated code patch for that task
│       └── submission_details.txt # include line "submitter_name: {name}" for leaderboard
├── scripts/
│   ├── build_leaderboard.py      # renders docs/index.html from results.csv
│   └── evaluate_submission.py    # grades a PR & appends a row to results.csv
├── templates/             # Jinja2 templates used by the builder
│   └── leaderboard.html.j2
├── docs/                  # GitHub‑Pages artefacts (auto‑generated)
│   └── index.html
└── .github/workflows/     # CI jobs (grading + deploy)
    ├── evaluate.yml
    └── leaderboard.yml
```

---

## 2  How to submit a model

1. **Fork & clone** the repository.
2. Inside the top‑level `submissions/` directory create **one folder** named exactly what you’d like to appear in the leaderboard.  For example, if your model is called *CoolModel‑v2*:

   ```bash
   mkdir -p submissions/CoolModel-v2
   ```
3. For **every task** you solved, add a sub‑folder whose name is that task’s ID, and drop a single `patch.diff` file produced by your model:

   ```bash
   mkdir -p submissions/CoolModel-v2/25570_1192
   cp /path/to/patch.diff submissions/CoolModel-v2/25570_1192/
   ```
4. Commit & open a **pull request**.

The `evaluate.yml` workflow will spin up, run `scripts/evaluate_submission.py`, and:

* verify your folder structure
* compute Earned/Accuracy metrics
* append a new row to `data/results.csv` (using your top‑level folder name as **Model**, and submitter_name as submitter) and push it back to the PR branch
* trigger `leaderboard.yml` to rebuild `docs/index.html`

Once the PR is merged, the leaderboard on GitHub Pages updates automatically (~1 minute).

---