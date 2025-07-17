# SWE‑Lancer Leaderboard

Access the current leaderboard [here](https://swelancer.github.io/leaderboard/)

This repository contains **(a)** the SWE‑Lancer benchmark data, **(b)** an automated grading workflow, and **(c)** the public leaderboard served via GitHub Pages.

---

## 1  Repository layout

```
<repo‑root>/
├── data/                  # Ground‑truth data & aggregated results
│   └── results.csv        # ← generated from submission folder; DO NOT EDIT BY HAND
├── submissions/           # Community submissions land here (see §2)
│   └── <DisplayName>/     # one folder per submission, name = what shows on LB
│       └── <task‑id>/     # one folder per task, e.g. 25570_1192
│           └── patch.diff # model‑generated code patch for that task
│       └── submission_details.txt # include line "submitter_name: {name}" for leaderboard
├── scripts/
│   └── build_leaderboard.py      # renders docs/index.html from results.csv
├── templates/             # Jinja2 templates used by the builder
│   └── leaderboard.html.j2
├── docs/                  # GitHub‑Pages artefacts (auto‑generated)
│   └── index.html
└── .github/workflows/     # CI jobs (grading + deploy)
    └── leaderboard.yml
```

---

## 2  How to submit a model

1. **Fork & clone** the repository.
2. Inside the top‑level `submissions/` directory create **one folder** named exactly what you’d like to appear in the leaderboard.  For example, for the o1 submission, you would do

   ```bash
   mkdir -p submissions/o1
   ```
3. For **every task** in the offline subset (all 198), add a sub‑folder whose name is that task’s ID, and drop a single `patch.diff` file produced by your model.  See the o1 submission folder for an example of how to do this, but you should end up with file paths such as:

submissions/o1/25570_1192/patch.diff

4. Add in a submission_details.txt file.  In this file, the top line should be "submitter_name: {name}", where name will appear as the submitter on the leaderboard. Underneath this, feel free to provide additional information, such as author names, links to appropriate repos, etc.

5. Commit & open a **pull request**.

We will
* verify your folder structure
* verify your submissions
* compute Earned/Accuracy metrics
* append a new row to `data/results.csv` (using your top‑level folder name as **Model**, and submitter_name as submitter) and push it back to the PR branch

Once the PR is merged, the leaderboard on GitHub Pages updates automatically (~1 minute).

---
