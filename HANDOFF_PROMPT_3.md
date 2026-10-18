# HANDOFF PROMPT 3 (updated 18 October 2026): continue the F1 podium project (paste this into the new conversation)

You are **Claude Code inside VS Code** on a Windows machine, continuing, as the same assistant, a project that our university team has been building with Claude in earlier conversations. **Several team members work on the same files** (git authors so far: Hoor Sobh and esraa), so always check `git log` and what is on disk before you trust anything, including this prompt. Do **not** change anything until you have finished Part 1 and given the summary in Part 11. Then wait for an answer.

Project folder: `C:\Users\harho\OneDrive\Desktop\ACL 2\VSCode` (git, remote `https://github.com/esralsayed/ACL-milestone1.git`, branch `main`).
**Deadline: 18 October 2026, 11:59 PM (today, when this prompt was written).** Read Part 10 (time) first.

This prompt replaces `HANDOFF_PROMPT.md`, `HANDOFF_PROMPT_2.md` and the earlier version of this file (in git history).

---

## PART 1: READ FIRST

1. `M1 Desc.pdf` (the brief) and `ACL formula 1 intro.pdf` (the introduction). Use `/mingw64/bin/pdftotext -layout "<file>" -` (not UTF-8; "�" is `<=`, `>=` or a dash).
2. **`F1_decisions.md`** (about 1,380 lines): plan, 74 decisions in tables A-M (last column = what was chosen, `open`, or "Deferred"), a "Why <ID>" section per decision with the numbers, experiments X1-X9, 33 edge cases. Its tables are padded: edit a row with a regex such as `^\| L8\s+\|.*$` and replace the last cell.
3. **`F1_podium_prediction.ipynb`** (**395 cells**, 172 code). Dump it with a Python script (index, type, id, number of outputs, full source) into the scratchpad and read all of it, at least cells 300-394 in full.
4. Background only: `README.md`, `F1_project_explained.md`, `F1_data_overview.md`, `F1_table_reference.md`, `F1_EERD.md`, the two SVGs, the older handoff prompts.
5. `git log --oneline` and `git status`. Last known HEAD: `10bddac till l7` (before it: `bde5732 updated handoff`, `168dd0e last 2 in J remain`). The team commits; never commit or push unless asked.
6. `.venv`: pandas 3.0.6, numpy 2.5.3, matplotlib, seaborn, scikit-learn 1.9.1, scipy, shap 0.52, lime, ipykernel. **Not installed:** statsmodels, PyTorch, TensorFlow, Keras. Run `.venv/Scripts/python.exe` with `PYTHONIOENCODING=utf-8`.
7. Memory note: report evidence for **all years (1950-2024) first**, later periods only as labelled extras.

**Verify, and report anything that differs:** 395 cells, the last one is the markdown "**Result (L7, validation 2020-2021, untuned):**"; code cells with saved outputs: 129, the last one is cell 318 (J3; execution counts 71-202); **no saved outputs** in cells 240-241 (Q2 answer) and 321-393 (everything from J4 on). `F1_decisions.md`: "Decided so far" ends with "K1, ..., K6, L1, ..., L7"; open: **L8, L9, L10, M1-M4**; deferred: **D2**.

---

## PART 2: HOW WE WORK (these override politeness)

**Professional standards**
- Act as a professional data analyst, not an assistant who agrees. If a request is weaker than an alternative, wrong, or hides a risk, say so with evidence **before** doing it; if the team insists, do it and state the limitation in the notebook and the md.
- Check every step for leakage (known before the race?), grain (one row per driver per race), missingness, selection bias, era effects, sample size, proof versus proxy.
- **Every number, count, name or year must come from code you ran on the CSV files or from a saved notebook output. Never add up numbers by hand** (this caused wrong totals once). If you correct a number, say so and fix every place it appears.
- **No outside Formula 1 knowledge as evidence.** If unavoidable (the 9 nationality links of I1, the meaning of a status word in J1), label it **"not from the data"**. The introduction and the brief are allowed sources: quote them.
- Never refer to a file, column, cell, variable or decision you have not opened.
- Every team member can be asked about any step, and "an AI tool suggested it" is not accepted: every claim needs a number and a simple explanation.
- When a request can be read two ways, **state the reading you use**. Use "they/them" for people whose pronouns are not stated.
- **All-years evidence first**, unless the question fixes the years (Q1: 2003-2024 by H2; Q3: 2014-2024; models: the split of K1).

**The decision loop**
1. The team names the decision. 2. Explain step by step in simple English with **real rows and numbers** (a real example: one driver, one race, one team). 3. Options table with numbers, the cost of each rejected option, **one recommendation**. 4. **Wait for the choice; record only after it is confirmed.** 5. When a decision picks a number, justify it **by trial and error on the data** (several values in one notebook cell, as in H3, J4, L7); if a number is a convention, say so. 6. Then add notebook cells (markdown "How we came to this question", code with the evidence, markdown "Result" + "Decision" + reasons + rejected options + limit), unless told "md only", and always edit `F1_decisions.md` (the row's last cell, the "Decided so far" line, a "Why <ID>" section before the next group heading).

**Phases**
- Cleaning and feature definition: counts and descriptive statistics only, no model scores. In step 10 (where we are now) choices are made **on validation 2020-2021 only**, with PR-AUC (primary, K2) and its 95% range from resampled races (`race_samples`). **The test seasons 2022-2024 have never been used for any choice and must not be, until the final comparison.**
- Something the team calls "a modelling-phase question" is recorded as deferred, not decided.
- Raw CSVs are immutable. The notebook assumes no domain knowledge: every claim is discovered by code first.

**Style:** simple English, short sentences, tables, real numbers. No complexity that was not asked for (e.g. J1 has no sensitivity check because the team said so). Do not commit or push.

---

## PART 3: TECHNICAL GOTCHAS

1. **VS Code overwrites notebook edits** if the notebook is open with unsaved changes. Before editing check the cell count and the last cell on disk; after every write tell the user: close the notebook without saving (or `File: Revert File`), reopen, check the cell count, then Ctrl+S. Teammates may edit too: check `git status` first.
2. **Edit the notebook with a Python script:** load the JSON, `assert` the expected count and last cell, `assert` the new section is not already there, append cells with fresh ids (`secrets.token_hex(4)`), `execution_count: None`, `outputs: []`, `metadata: {}`; write with `json.dump(nb, f, indent=1, ensure_ascii=False)`. `NotebookEdit` fails on this notebook.
3. **Write scripts and cell sources with the Write tool, never long bash heredocs** (quotes and `\N` break them). Cell sources as raw strings in a `.py` file: `CELLS = [("markdown", r'''...'''), ("code", r'''...''')]`. Temporary files go in your scratchpad directory.
4. **Test every new code cell before inserting it** with a harness (rebuild it): run all existing code cells in order in one namespace (backend `Agg`, `display` prints `.to_string()`, `plt.show` saves PNGs for the new cells only, the last expression of each cell is printed), then the new cells; read the output before writing any interpretation. **Running all 395 cells now includes model fits and bootstraps: measure the time** (the 316-cell version took about 35-50 s). Look at every plot as a PNG before describing it.
5. `\N` in Python source: `chr(92) + "N"`.
6. pandas 3: `groupby(...).apply(..., include_groups=False)`; raw tables are text (`text[...]`). **`raceId` is not in date order**: sort by `date`. Rolling windows: `s.shift(1).rolling(N, min_periods=1)`.
7. Sanity-check printed numbers (a `max`/`min` slip once printed 2024 instead of 2003).
8. **Names redefined by later cells** (the last definition wins in a Run-All; do not rely on the earlier one): `best_f1_threshold` (cell 351 returns `(threshold, best F1)`, cell 355 returns the threshold only), `BASE_FEATURES` (cell 336: with `field_size`; cell 381: `base_podium_chance` instead), `QUALI_FEATURES` (cell 336: position, gap, flag; cell 367: position and flag only), `FEATURES_L1`, `VARIANTS`, `MODELS`, `trial`, `rows`, `both`, `summary`, `ranked`, `zero`, `table`, `changed`, `started`, `season_of`, `starters`, `colors`, `order`. **The X1, K2-K6, K3/D3 and L1 results were computed with the qualifying gap and field size; L5-L7 with the final 16 features.**
9. Kaggle: `DATA_DIR = Path("csvs")` and the relative image `F1_relationships.svg` must work there (path variable, uploaded file or PNG).
10. Cells 240-241 and 321-393 have never been run in Jupyter. A full Restart-and-Run-All is still to do.

---

## PART 4: THE PROJECT

**Milestone 1: Formula 1 podium prediction.** Kaggle/Ergast data 1950-2024, 14 CSV tables in `csvs/`. **Unit:** one driver in one race. **Target:** `positionOrder <= 3`. **Cutoff:** after qualifying, before the race.

**Brief checklist (what must be in the notebook and report):** EDA **before and after** cleaning with plots; `\N` cleaned, semantic typing (dates, lap times in seconds); one row per `(raceId, driverId)`; keys checked; Q1-Q3 with multi-hop joins, plot, answer, grain/missingness/cutoff note; features justified with evidence, a leakage-safe form feature, "plotting the effect of the features", "effect of the step on data distribution/range/values"; a justified split; at least two statistical models + a shallow neural network (1-2 hidden layers), a baseline, at least three distinct modelling attempts; ROC-AUC, PR-AUC, F1 (+ precision, recall, K4) on train/validation **and** the unseen test; thresholds and hyperparameters from train/validation only; feature-group ablation; at least two preprocessing-order experiments; XAI: permutation importance + SHAP (global), LIME and/or local SHAP (local), "importance is not causation"; an inference function on a complete and a partially missing record; **PDF report** (Q1-Q3 answers with figures, selected features and why each is valid pre-race, limitations incl. "historical qualifying-coverage drift, era sensitivity"); run-all notebook. **Submission:** public Kaggle notebook link + GitHub repo link + PDF via `https://forms.gle/esDxHsvfzffYHVAZ9`.

**Notebook outline (395 cells; cell index):** loading (0-4); missing values (5-53); formats (54-97); keys (98-104); duplicates B1-B4 (105-155); EDA before cleaning, 6 analyses (156-183); row filters C1, C2, C3, C6, C7, "Applying the filters" (184-210); labels A5 (211-218); home race I1, I2, I5 with table `q2` (219-231); Q2 control I4 (232-238); **Q2 answer (239-242)**; E6 (243-248); standings F1-F3 (249-256); F4 (257-261); G2 (262-266); G4 (267-269); G5 (270-274); G7 (275-280); G9 (281-284); **Q1**: H1 (285-291), H2 (292-296), H3 (297-301), answer (302-306); **Q3**: J1 (307-311), J2 (312-315), J3 (316-319), **J4 (320-325), J5 (326-329), answer (330-334)**; **modelling**: K1/C4/X1 (335-341), rolling-validation check (342-345), K2 (346-348), K4/K5/K6 (349-353), K3/D3 (354-356), L1 (357-364), E4 revisited, gap removed (365-368), L2 (369-373), L3 (374-376), L4 (377-379), G10 updated, `base_podium_chance` (380-382), L5 baseline (383-385) + follow-up (386-388), L6 (389-391), L7 (392-394).

**Key variables** (run earlier cells first): `text`, `results_one_row` (26,668), `status_name`, **`clean_rows`** (24,652; the model rows and the source of all form history, G8), `drivers_clean`/`circuits_clean`/`constructors_clean`, `q2` and `home` (Q2), `races_by_date`, `previous_race`, **`rows_f`** (`rank_before`, `points_before`, `previous_race`), **`rows_t`** (`team_rank_before`, `state`), **`form_measures`** (per row `podium`, `relative_place`, `finished`, `earlier_starts`, last-5 driver form), `q1`, `wilson(k, n)`, `q3` (with `mechanical`, `start`), `starts`, `team_rates`, `MIN_STARTS` (34), `q3_rates`, `sprint_q3`.
**Modelling variables:** **`x1_table`** (all 24,652 rows of `clean_rows`, all years incl. the test seasons, with the features), `team_form`, `quali_times`/`lap_seconds` (q-times in seconds), **`BASE_FEATURES`** (10: `grid`, `base_podium_chance`, `rank_before`, `team_rank_before`, `podium_last5`, `relative_place_last5`, `finished_last5`, `team_podium_last5`, `team_relative_place_last5`, `team_finished_last5`), **`QUALI_FEATURES`** (`quali_position`, `has_qualifying`), **`FLAGS`** (`rank_was_empty`, `team_rank_was_empty`, `first_start`, `team_first_race`), **`FEATURES_L1`** (the 16 features), `logistic()`, **`race_samples(rows, n=1000, seed=42)`** (resampled races for 95% ranges), `validation`, **`y_val`**, `val_pred`, `VARIANT_D`, `best_f1_threshold`, `l1` (x1_table + `previous_race`, `points_before`, `state`, `earlier_starts`), **`fill_empty(rows, train_rows)`** (L1), **`l1_filled`**, **`l1_trn`** (≤ 2019, filled), **`l1_val`** (2020-21, filled), `drivers_listed`, `teams_listed`, `scaler`, **`baseline`** (fitted logistic regression pipeline), **`tree_table`/`tree_trn`/`tree_val`** (empty values left empty + flags, for the tree models), `l6_models`.

---

## PART 5: THE DATA (all verified by code)

- Raw: races 1,125 (1950-2024), results 26,759, qualifying 10,494 (from 1994; every race has it from 2003), sprint_results 360 (18 sprints, 2021-2024), driver_standings 34,863, constructor_standings 13,391 (from 1958). 14 primary keys, 23 foreign keys valid.
- Rows: 26,759 → B1 26,668 → C1 (−1,635 `grid = 0`) → C3 (−381 Indy 500) → **24,652 rows, 3,344 podiums (13.6%)**; 1,112 races with exactly 3 podium rows, 2 with 4 (shared cars of 1951 and 1955).
- **Split (K1):** training 1950-2019 (22,570 rows, podium rate 13.4%), validation 2020-2021 (763 rows, 39 races, 117 podiums, 15.3%), test 2022-2024 (1,319 rows, 68 races, 204 podiums). A validation PR-AUC has a 95% range about 0.24 wide.

---

## PART 6: DECISIONS (see the md for numbers; 66 decided, D2 deferred, L8-L10 and M1-M4 open)

| ID | Decision |
|---|---|
| A1-A5 | `\N` and blank = missing; lap times in seconds; mixed-format columns not used; keep lists; 3 label corrections |
| B1-B4 | Lowest `resultId` row per driver-race; grid/team from it; sharers both keep a place; no renumbering |
| C1-C3, C6, C7 | Remove `grid = 0` (1,635); keep grid slot + 0 laps; remove Indy 500; keep disqualified; sprints not features |
| **C4** | **By X1: the models train on all seasons 1950-2019 with the qualifying features** (variant d; empty + `has_qualifying`) |
| C5 | Q1-Q3 start from `results_one_row` without Indy (Q1 no filter; Q2 `grid > 0` = `clean_rows` pairs; Q3 2014-24, starts = not `W`); models use `clean_rows` |
| D1 | Target `positionOrder <= 3` |
| D2 | **Deferred** to step 10: nothing / class weights / resampling |
| **D3** | **Not forced to 3 per race; "top 3 per race" reported as an extra F1 column** |
| E1-E3, E5, E6 | As before (no `grid = 0` rows; qualifying empty + `has_qualifying`; grid and qualifying position two groups; team = `results.constructorId`) |
| **E4** | **Revisited: the qualifying gap is removed** (rank corr 0.88 with the position; +0.009 PR-AUC, −0.003 to +0.020). X3 and X4 dropped |
| F1-F6 | Previous race by date; no standings row = 0 points; team standings empty before 1958; rank and share of leader built (X6); use `position` |
| G1-G9 | 5 windows (only **last 5** built so far), driver + team form, follow `constructorId`, current team, empty without history, G6 by X7, G7 podium share + relative place + finish rate, G8 history from `clean_rows`, G9 no circuit history |
| **G10** | **`base_podium_chance` = 3 ÷ starters replaces field size** (podium rate = 3 ÷ starters within 0.17 points in every era); year/era by X9 |
| H1-H3 | Q1: both front rows; 2003-13 vs 2014-24; ≥ 5 races per period (14 circuits) |
| I1-I5 | Q2: 25 nationality links; dual = either; `USA` merged; grid bands + Mantel-Haenszel; "never home" rows stay |
| J1-J3 | Q3: 47 mechanical statuses (416 rows); start = not `W`; one team = one `constructorId` |
| **J4** | **A team is ranked with ≥ 34 starts in the period** (one full season, 2 × 17 races); top 3 identical for minimums 34-75 |
| **J5** | **Sprint failures not counted** (60 / 299 sprint starts, 1 / 3 mechanical; no top 3 changes) |
| **K1** | **The introduction's split:** train ≤ 2019, validation 2020-21, test 2022-24; every validation score with its 95% range; rolling validation 2018-21 was a check only |
| **K2** | **PR-AUC primary, ROC-AUC secondary** (12 X1 runs: PR-AUC 0.657-0.728, ROC-AUC 0.914-0.930; they pick different winners) |
| **K3** | **Per model, the best-F1 threshold on validation, used unchanged on test** (0.22-0.38) |
| **K4** | **ROC-AUC, PR-AUC, F1 + precision and recall** (accuracy not used: "never a podium" = 84.7%) |
| **K5** | **No retraining on train + validation** |
| **K6** | **2020 is a normal season** |
| **L1** | **Fill + flag for logistic regression and the network, no fill for the tree models**, learned on training rows: qualifying position = grid; missing driver/team rank = last place (listed + 1), team rank before 1958 = training median; form with no earlier race = training median; 4 flags |
| **L2** | **Standard scaling on training rows** (logistic regression, network); trees not scaled |
| **L3** | **IDs dropped as model inputs** (21.8% of test rows have an unseen driver, 19.9% an unseen team) |
| **L4** | **Experiment 2: fill → scale vs scale → fill; experiment 3: filter → driver form (G8) vs driver form → filter** (10.2% of training rows change) |
| **L5** | **Baseline = logistic regression on all 16 features:** validation PR-AUC 0.706 (0.591-0.830); references: random 0.153, grid ranking 0.639 |
| **L6** | **Both random forest (leaves ≥ 20 rows) 0.723 and gradient boosting 0.713** (untuned; difference within chance); random forest kept if time is short |
| **L7** | **scikit-learn `MLPClassifier`, 1-2 hidden layers**, Adam/ReLU, `alpha`, early stopping; sizes 32, 64, 32+16, 64+32 left to L8 (all 0.707-0.716, seed spread up to 0.032) |

---

## PART 7: EXPERIMENTS (state)

| # | State |
|---|---|
| X1 | **Done** (variant d) |
| X2 | Covered by X1 and the ablation |
| X3, X4, X5 | **Dropped** (gap removed; X5 for time) |
| X6 | **Not run:** rank vs share of the leader's points (only rank is built) |
| X7 | **Not run:** form windows (only last 5 is built; last 3, 10, season so far, career not built) |
| X8 | Optional (cut first) |
| X9 | **Not run:** (a) base chance only, (b) + era, (c) + year |
| L4 exp. 2 and 3 | **Not run** (defined in L4) |
| Ablation | **Not run** (groups = L9, open) |
| D2 | **Not run** (class weights could be part of tuning, L8) |

---

## PART 8: EDGE CASES

The md lists 33 (some counts raw, before B1). Found later, not yet in the md table: `positionOrder` still counts rows removed by C1 (67 rows would have relative place above 1: G7 ranks among the starters); the 72 pit-lane starts are real races but not in `clean_rows` (C1, G8) and are counted in Q3 (J2); `laps = 0` cannot separate "failed on lap 1" (R) from "failed before the start" (W): 28 W rows in 2014-24, 15 with a mechanical status; Räikkönen 2017 Malaysia is R with grid 0 and 0 laps; 7 of the 38 qualifying-front-row drivers who did not start there are sprint weekends; Interlagos 2014-24 has 19 grid front-row starts in 10 races; same venue under two circuit IDs (none inside 2003-2024); Sauber's ID 15 covers 2014-2018 and 2024; Q3 status labelling shifts between periods (Collision damage 5.3% vs 13.9% of non-finishes); seasons 2014-24 have 17-24 races; Caterham (33) and Marussia (31) raced part of 2014; a sprint row has the letter `N` (not in the introduction's list) and a Haas sprint row is classified 20th with a car-part status; 1,553 training rows have no standings rank (615 first starts); 23 rows (round 1 of 1950) have no previous standings at all.

**Small inconsistencies to fix in the md when convenient:** the plan table still says steps 7, 8 and 10 are "To do"; the "Deferred to step 10" line still lists E3/E4 (both dropped); the L1 row still describes a gap fill (the gap was removed).

---

## PART 9: WHAT IS LEFT (in the order I recommend)

**Must do (brief requirements):**
1. **L8, L9, L10** (open): tuning on validation PR-AUC (small grid per model: random forest `min_samples_leaf`, `max_features`; gradient boosting `learning_rate`, `max_leaf_nodes`, `min_samples_leaf`; network sizes 32/64/32+16/64+32 × `alpha`; logistic regression `C`; class weight none/balanced if D2 is folded in); ablation groups (suggested: grid; qualifying = position + `has_qualifying`; standings = driver and team rank + their flags; driver form; team form; base podium chance); seed 42 (already used everywhere; report the seed spread of the network).
2. **Final model comparison:** 4 models (logistic baseline, random forest, gradient boosting, network) + the two reference rows, on **training, validation and test**: PR-AUC, ROC-AUC, F1, precision, recall (threshold from validation, K3), top-3-per-race F1 (D3), 95% ranges by race. Plot the PR curves.
3. **Feature-group ablation** (L9) and **the two preprocessing-order experiments** (L4), each attempt in its own cell.
4. **XAI (M1-M4 open):** permutation importance and SHAP on the best model (global), one local explanation (local SHAP waterfall, and LIME if time), interpreted; state that importance is not causation.
5. **Inference function:** input one record (suggested: a dictionary), apply the L1 fill and L2 scaling learned on training, return a probability and yes/no at the K3 threshold; a given grid of 0 → last slot (E1); demonstrated on a complete record and one with missing qualifying (and no history).
6. **EDA after cleaning** (brief: "this step should be done both before and after the cleaning"): repeat key plots on `clean_rows` / the modelling table with before/after counts. **Not done yet.** Also a short visible "semantic typing" summary (dates via `races_by_date`, lap times via `lap_seconds`).
7. **Restart-and-Run-All** in Jupyter (time it), fix errors, save outputs.
8. **PDF report**, **Kaggle** (public notebook, data paths, SVG), **GitHub** (team commits), **submission form**.

**Optional (cut first, in this order):** X8, X6, X9 (c), X7 beyond last 5, LIME (keep local SHAP), random forest or gradient boosting (L6: keep random forest), D2 as a separate experiment (fold into tuning).

**Questions the team may send to the teaching assistant:** three or five metrics; is the introduction's split binding; LIME required; is scikit-learn's MLP acceptable; what "preprocessing-order experiments" means. Our defaults are already what we do.

---

## PART 10: TIME

The deadline is **tonight, 18 October 2026, 11:59 PM**. The models are only partly built (untuned), and the test results, ablation, preprocessing experiments, XAI, inference function, EDA after cleaning, run-all, report and Kaggle are not done. Therefore:
- Propose **one batch** for L8-L10 and M1-M4 with defaults, get it confirmed, and build.
- Prefer a lean, complete notebook over extra experiments: every brief requirement once, with ranges and a short interpretation.
- Check the total Run-All time before adding heavy loops (bootstraps, seeds, grids): keep `race_samples` at 1000 or fewer and the tuning grids small.
- Teammates can work in parallel on the report and Kaggle: offer them text and figures.

---

## PART 11: WHAT TO DO NOW

1. Do Part 1 and the verification.
2. Reply with: (a) a short summary of where we are; (b) decisions taken, deferred and open; (c) anything in the files that contradicts this prompt or looks wrong; (d) a time plan for the rest of today with cuts; (e) any decision already taken that looks weak, with data.
3. Then propose the batch L8, L9, L10, M1-M4 (and D2) with defaults, and wait.
