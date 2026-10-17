# HANDOFF PROMPT 2: continue the F1 podium project (paste this into the new conversation)

You are **Claude Code inside VS Code** on a Windows machine, continuing, as the same assistant, a project that I (the team leader of a university team) have been building with Claude in earlier conversations. Do **not** change anything until you have finished Part 1 and given me the summary in Part 9. Then wait for my answer.

Project folder: `C:\Users\harho\OneDrive\Desktop\ACL 2\VSCode` (git repository, remote `https://github.com/esralsayed/ACL-milestone1.git`, branch `main`).
**Deadline: 18 October 2026, 11:59 PM.** At the time of writing it is **16 October 2026, so about 2 days remain.** Read Part 8 (time) before anything else, because it changes how we must work from now on.

---

## PART 1: READ FIRST (in this order, completely)

1. `M1 Desc.pdf` (the brief) and `ACL formula 1 intro.pdf` (the Formula 1 introduction). The Read tool returns nothing for PDFs: use `pdftotext` (`/mingw64/bin/pdftotext`, run with `-layout`, and with `-raw` for tables). Symbols shown as "�" are `<=` and `>=`.
2. **`F1_decisions.md`**: the most important file. It has the plan (10 steps), the 74 decisions (tables A to M; the "Decided" column says what was chosen), a reasoning section per decision (with the data), the list "Experiments to run in step 10" (X1-X8), and the 33 edge cases. NOTE: my editor reformatted its tables (columns padded to equal width, e.g. `| F4  |`), so any script that edits a row must match with a regex such as `^\| F4\s+\|`, never an exact string.
3. **`F1_podium_prediction.ipynb`** (about 271 cells). It is too big for the Read tool. Dump it with a short Python script (load the JSON, print each cell's index, type, id and full source). Read **all** cells.
4. `README.md`, `F1_project_explained.md`, `F1_data_overview.md`, `F1_table_reference.md`, `F1_EERD.md` and the two SVGs are early background documents, partly superseded (the notebook and `F1_decisions.md` win). `HANDOFF_PROMPT.md` is the first handoff prompt (older; this one replaces it).
5. `csvs/` (14 tables): look at the first rows and columns of each yourself.
6. `git log --oneline` and `git status`. Last known HEAD: `27f9005 history decisions` (I commit myself; never commit or push unless I ask).
7. `.venv`: pandas 3.0.6, numpy 2.5.3, matplotlib, seaborn, scikit-learn 1.9.1, scipy, shap 0.52, lime, ipykernel. **Not installed:** statsmodels, PyTorch, TensorFlow, Keras. Run Python as `.venv/Scripts/python.exe` with `PYTHONIOENCODING=utf-8`.

Then verify, and tell me if anything differs: the notebook has about 271 cells and ends with the section "A driver's first start: no history (decision G5)"; `F1_decisions.md` says "Decided so far: A1-A5, B1-B4, C1, C2, C3, C6, C7, D1, E1, E2, E3, E4 (partly), E5, E6, F1-F6, G1-G5, I1-I5" and 74 decisions in total.

---

## PART 2: HOW I WANT YOU TO WORK (read twice; these override politeness)

**Professional standards**
- Work as a professional data analyst, **not as an assistant that agrees with me.** If something I ask is weaker than an alternative, wrong, or hides a risk, say so with the evidence **before** doing it. If I insist after the evidence, do it my way and note the limitation.
- Check soundness every time: leakage (is it known before the race?), grain (one row per driver per race), missingness, selection bias, era effects, sample size, proof versus proxy.
- **Every number, count, name or year you give me must come from code you ran on the CSV files** (or from an output already in the notebook). Never recall a number from memory. If you correct an earlier number, say so plainly and fix every place it appears.
- **Do not use outside Formula 1 knowledge as evidence.** If you must use domain knowledge (for example the nine nationality-to-country links, or why a team was renamed), say it is **"not from the data"** and keep it labelled. The introduction PDF and the brief are allowed sources; quote them.
- Never refer to a file, column, cell, variable or decision you have not opened and verified.
- **In this team every member can be asked about any step, and "an AI tool suggested it" is not accepted.** So every claim needs a number, and I must be able to explain it simply.
- When two readings of my words are possible, state the one you are using. Use "they/them" for people whose pronouns are not stated.

**How we take a decision (the loop we have followed for each decision)**
1. I say "move to the next decision" (or name one).
2. You **explain first, step by step, in simple English**, using **real rows and numbers from the data**, and say *why* the decision exists at all. I often ask "explain simply", "explain from the beginning", or "elaborate": do it with a toy-style example built from real data.
3. You lay out the **options in a table with numbers for each option**, say what each rejected option costs, and **recommend one**.
4. **You wait for my choice. You record a decision only after I confirm it.** (Mistake to avoid: once I recorded E6 as decided before I had confirmed; I had to revert it. Never present an undecided item as decided.)
5. After I choose, I usually say one of: "add a stats/code cell with the justification" (then add notebook cells: a markdown cell that says how we came to the question, one or more code cells with the evidence, and a markdown cell with the result and the decision with reasons, plus why the other options were rejected), or "just mark it in the md" (then only edit `F1_decisions.md`). Always also edit `F1_decisions.md`: the row's "Decided" cell, the "Decided so far" line, and a "Why <ID>" reasoning section with the numbers (placed before the next group heading, currently before `### H. Question 1`).
6. Then I say "move to the next decision".

**Rules about models and phases (I corrected you on this twice)**
- In the cleaning and feature-definition phases **do not fit models and do not compare options by predictive score** (not even the AUC of one column alone). Use counts, rates and descriptive statistics only. Anything that compares options by how well they predict is an **experiment for step 10** (see the list X1-X8 in `F1_decisions.md`). If you ran a quick exploratory check, label it "exploratory, not evidence" and keep it out of the justification.
- Raw CSV files are immutable; cleaning happens on copies.
- The notebook must assume **no domain knowledge**: every claim about the data is first discovered by code in the notebook.

**Style:** simple English, short sentences, tables for options, real numbers. When I say "explain like I'm 5", use toy-car analogies with real numbers. Do not add complexity I did not ask for, but tell me when the simple approach hides a risk. Do not commit or push.

---

## PART 3: TECHNICAL GOTCHAS (learned the hard way)

1. **VS Code overwrites your notebook edits** if the notebook is open with unsaved changes. After every write, tell me: close the notebook **without saving** (or `File: Revert File`), reopen, check the **cell count**, and only then press Ctrl+S. Before adding cells, check what is on disk (cell count and last cell).
2. **Edit the notebook with a Python script** (load the `.ipynb` JSON, append cells with fresh 8-character ids, `execution_count: None`, `outputs: []`, write back with `json.dump(nb, f, indent=1, ensure_ascii=False)`; assert the section is not already inserted). `NotebookEdit` fails on this notebook.
3. **Write scripts with the Write tool, not bash heredocs**: long scripts with apostrophes and backslashes broke the shell quoting several times. Keep temporary scripts in the scratchpad directory given in your own system prompt (it will differ from the old one).
4. **Test every new cell** before you insert it: execute the notebook's earlier code cells in order in one namespace (set `display` to a function that stores the object, `plt.show` to a no-op, matplotlib backend `Agg`), then your new cell, and **read the output before you write the interpretation**. Every number in the notebook text must come from that output. This is not a full Restart-and-Run-All; the new cells have **no saved outputs**; a full run-all in Jupyter is still to do (check run time: `lap_times.csv` is 16.8 MB).
5. **Backslash trap:** the placeholder is the two characters `\N`. In Python source use `chr(92) + "N"`; `"\N"` is a syntax error. Windows console is cp1252: set `PYTHONIOENCODING=utf-8`.
6. **pandas 3:** `groupby(...).apply(..., include_groups=False)`; text columns have dtype `str`. Watch for merge column clashes (`position` exists in both `results` and `qualifying`; `raceId` in two frames), and string versus integer keys: all raw tables are loaded as text.
7. `F1_decisions.md` tables are padded (see Part 1): match rows with a regex.
8. The notebook is shared with the browser/Kaggle plan: `DATA_DIR = Path("csvs")` and `F1_relationships.svg` (relative link) must be made to work on Kaggle (path variable, uploaded file or PNG).
9. To check a plot, render it to PNG and look at it before describing it.

---

## PART 4: THE PROJECT

**Milestone 1: Formula 1 podium prediction.** Data: Kaggle/Ergast Formula 1 World Championship 1950-2024, 14 linked CSV tables in `csvs/`. **Unit:** one driver in one race. **Target:** `positionOrder <= 3`. **Cutoff:** after qualifying, before the race: only information known at that moment may be a feature (the race's own result, points, laps, status, pit stops and standings are leakage; anything from earlier races is allowed).

**Brief checklist:** EDA before and after cleaning with plots; clean `\N`, semantic typing (dates, lap times to seconds); exactly one row per `(raceId, driverId)`; primary and foreign keys checked; three data-engineering questions (Q1: which circuits convert a front-row start into a podium, and does the ranking change after 2014, distinguishing qualifying from grid; Q2: do drivers podium more at home after controlling for starting position; Q3: which constructors have the highest mechanical-retirement rate in 2014-2021 against 2022-2024); feature selection justified with evidence and a leakage-safe form feature; an appropriate train/validation/test split, justified (the introduction suggests train <= 2019, validation 2020-2021, test >= 2022); at least two statistical models plus a shallow neural network (1-2 hidden layers), a baseline, at least three distinct modeling attempts, metrics ROC-AUC, PR-AUC, F1 (the brief also says "all five metrics": add precision and recall), on train/validation and on unseen test, thresholds and hyperparameters from train/validation only; a feature-group ablation and at least two preprocessing-order experiments; XAI: permutation importance and SHAP (global), LIME and/or local SHAP (local), stating that importance is not causation; an inference function shown on a complete and a partially missing record; a **PDF report** (answers to Q1-Q3 with figures, selected features and why each is valid pre-race, limitations); a run-all notebook. **Submission:** public Kaggle notebook link + GitHub repo link + the PDF report, through `https://forms.gle/esDxHsvfzffYHVAZ9`.

**Notebook outline (about 271 cells):** loading as text; first look; missing values per table; formats per table; keys and links; duplicates (rule B1 and its checks); EDA (6 analyses with a justification cell before each, summary table); "Cleaning: which rows stay" (C1, C2, C3, C6, C7, then "Applying the filters" with the row-count log); text-label cleaning (A5); "The home race" (I1, I2, I5) and "Question 2: controlling for the starting position" (I4); E6; "Standings before the race" (F1, F2, F3); "Team standings before 1958" (F4); "Driver form and team form" (G2); G4; G5. Decisions **without** notebook cells (only in the md): C4 (deferred), E2, E5, F5, G1, G3. You can add notebook cells for them if I ask.

**Key variables defined by notebook cells** (later cells depend on them; earlier cells must run first): `text` (all raw tables as strings), `results_one_row` (26,668 rows, strings), `eda` (ints, `year`, `podium`, `era`), `ERA_BINS`/`ERA_LABELS`, `with_q`, `status_name`, `rows` (in the C3 cell; has race `name`), `table` (C6 cell), **`clean_rows`** (after all row filters, 24,652 rows), `drivers_clean`/`circuits_clean`/`constructors_clean` (A5), `nationalities`, `countries`, `links`, `nationality_to_country`, `by_spelling`, `dual`, `home` (home-race flag, grid bands), `races_by_date` and `previous_race` (F1), `rows_f` (standings before the race, `points_before` filled with 0), `team_standings`, `team_results`, `rows_t` (F4), `form_rows`, `team_races` (G2), `changes` (G4), `history` (G5).

---

## PART 5: THE DATA PIPELINE SO FAR (all numbers verified by code)

- Raw sizes: seasons 75, circuits 77, drivers 861, constructors 212, status 139, races 1,125 (1950-2024), results 26,759, qualifying 10,494 (494 races, 1994 onward; complete from 2003), sprint_results 360 (18 races, 2021 onward), driver_standings 34,863, constructor_standings 13,391 (1958 onward), constructor_results 12,625 (1958 onward), lap_times 589,081, pit_stops 11,371.
- Keys and links all valid (14 primary keys, 23 foreign keys). `\N` is the only placeholder; blank cells only in `qualifying.q2`/`q3`.
- **Row pipeline:** raw results 26,759 → **B1** keep the first row (lowest `resultId`) of the 85 repeated driver-race pairs → 26,668 rows (podium rows 3,379) → **C1** remove 1,635 rows with `grid = 0` → 25,033 (13.5% podium) → **C2** nothing removed (keep 966 rows with a grid slot and 0 laps) → **C3** remove the Indianapolis 500 (381 rows, 11 races, 35 podium rows) → **24,652 rows, 3,344 podium rows (13.6%)** → **C6** nothing removed (146 disqualified/excluded rows stay) → **C7** nothing removed (341 rows in sprint weekends stay; sprint results are not used as features).
- From 2003 on: 8,884 rows, 1,284 podium rows (14.5%), 428 races.
- Qualifying: `has_qualifying` (boolean, True when the driver has a qualifying row): 10,407 True, 14,245 False (E2).

---

## PART 6: DECISIONS ALREADY TAKEN (37 of 74)

(Details, numbers and rejected options are in `F1_decisions.md`; do not re-open them without evidence.)

| ID | Decision |
|---|---|
| A1 | Missing = `\N` and blank text |
| A2 | Lap times to seconds (`1:26.572` to 86.572) |
| A3 | Mixed-format time columns (`results.time`, `pit_stops.duration`, `positionText`) not converted/used |
| A4 | Keep only: races (`raceId, year, round, circuitId, name, date`), results (`raceId, driverId, constructorId, grid, positionOrder, points, statusId`), qualifying (`raceId, driverId, position, q1, q2, q3`) (note: `laps` is used for exploration only; the A4 list was found incomplete for Q2/Q3, which also need `circuits.country`, `drivers.nationality/dob`, `status.status`) |
| A5 | Explicit dictionary of 3 label corrections (`'Argentinian '` to `Argentine`, `United States` to `USA`, `&amp;` to `&`); copies `*_clean`; accents and names untouched |
| B1-B4 | Keep the first `resultId` row of a repeated pair; grid and team from the same row; keep both drivers who share a finishing place; no renumbering of places |
| C1 | Remove every row with `grid = 0` |
| C2 | Keep rows with a grid slot even with 0 laps (never filter rows with this race's `laps`/`status`: post-race) |
| C3 | Remove the Indianapolis 500 |
| C5 | Follows from C4: Q1-Q3 use the full cleaned table; only the models use a training window |
| C6 | Keep disqualified/excluded rows (label = official classification) |
| C7 | Do not use sprint results as features (0 rows up to 2019; pre-race, not leakage; stated limitation) |
| D1 | Target = `positionOrder <= 3` |
| E1 | No `grid = 0` rows in the table; the prediction function treats a given `grid` of 0 as a pit-lane start and uses the last slot |
| E2 | Cleaned table: no fill and no row dropped; qualifying columns empty where missing; boolean `has_qualifying`. The fill is experiment X5 |
| E3 | Keep `q1`-`q3` as seconds; one number = best of the three (whether best or `q1` only is experiment X3) |
| E4 (partly) | Gap to the fastest driver of the race; seconds, percent and a cap at the training 99th percentile are compared in step 10 (X4); the data check favours percent (pole time correlates +0.59 with the gap in seconds, -0.06 with the gap in percent) |
| E5 | Grid position and qualifying position kept as **two feature groups** (their model scores are preliminary; repeated as the ablation in step 10) |
| E6 | Team = `results.constructorId` (qualifying flips between IDs 206/209 in 2015) |
| F1 | Previous race = latest earlier date (all races in `races`) |
| F2 | Follows from F1: round 1 takes the previous season's final standings |
| F3 | No standings row = 0 points (1,169 "not started yet" + 408 "started, 0 points" = 1,577 rows; no contradiction) |
| F4 | Team standings left empty before 1958 (1,182 rows); whether used depends on the training window and split |
| F5 | No raw points; build **rank** and **share of the leader's points**; compare in X6 |
| F6 | Use `position`, ignore `positionText` in standings |
| G1 | Build five windows of form: last 3, last 5, last 10, season so far, career (earlier races only); choose by X7 |
| G2 | Build both driver form and team form, as two groups |
| G3 | Follow `constructorId`; renames reset history (the introduction says so); lineage table optional (X8) |
| G4 | Team form = the current team of the driver in this race |
| G5 | No earlier start gives an empty form value; a window with only some history uses the races that exist |
| I1 | Nationality-to-country table of 25 links (16 by spelling, 9 by knowledge: British-UK, French-France, American-USA, Spanish-Spain, Australian-Australia, Austrian-Austria, Dutch-Netherlands, Swiss-Switzerland, Monegasque-Monaco; the nine are "not from the data") |
| I2 | A dual-nationality driver is at home if the circuit is in either country |
| I3 | `USA` and `United States` merged (via A5) |
| I4 | Home effect compared inside grid bands 1-3, 4-6, 7-10, 11-15, 16+ with a pooled Mantel-Haenszel odds ratio; result: 0.93 (95% range over resampled races 0.78-1.07), so no clear home advantage; weighted difference -0.5 points against -2.1 raw |
| I5 | Rows of drivers whose nationality has no circuit country stay, with "home race" = False (2,344 rows, 46 drivers) |

---

## PART 7: WHAT IS LEFT

**Open decisions (35 of 74):**
- **G6** (reset the form at the start of a season, or carry over): I was in the middle of it. Recommendation given and **not yet confirmed by me**: option C, the rolling windows (last 3/5/10, career) carry over the season boundary and only "season so far" resets (consistent with G1 and with F1/F2, where the standings bridge round 1). Ask me to confirm.
- **G7** (what the form measures: podium share, average finishing place, points, DNF rate), **G8** (do past non-starts count), **G9** (circuit history), **G10** (era/year as a feature).
- **D2** (class weights for rare podiums), **D3** (force exactly 3 per race; 4 races have 4 podium rows).
- **H1-H3** (Q1: front row by grid, by qualifying, or both; which years count as before 2014; minimum races per circuit; note the same venue under two IDs: Zeltweg/Red Bull Ring 2.2 km apart, the two Las Vegas circuits 0.2 km apart).
- **J1-J5** (Q3: mapping from the 62 statuses of 2014-2024 to "mechanical" (unclear ones: `Retired`, `Technical`, `Damage`, `Collision damage`, `Puncture`, `Out of fuel`; note 7 podium rows have a non-finish status); denominator = race starts (grid slot); per `constructorId` (consistent with G3); minimum starts; sprint failures).
- **K1-K6** (split: the introduction's train <= 2019 / validation 2020-21 / test >= 2022 gives, with the 2003+ window, train 6,802 rows (963 podiums), validation 763 (117), test 1,319 (204); my recommendation was this split with bootstrap intervals by race (validation is small: the PR-AUC of the grid alone moves by about ±0.054); alternatives: validation 2018-21, validation 2018-19 only, a bigger test, rolling-by-season for tuning only; main metric PR-AUC and second ROC-AUC; threshold chosen on validation; add precision and recall; retrain on train+validation; 2020 as a normal season).
- **L1-L10** (missing-value fill learned on train only, scaling, ID encoding, two preprocessing orders, baseline, second statistical model, neural network library (only scikit-learn's `MLPClassifier` is available), tuning on validation, feature groups for the ablation (grid, qualifying, standings, driver form, team form), seed), **M1-M4** (model to explain, local example, input format of the prediction function, partially missing record).

**Deferred to step 10 as experiments** (listed in `F1_decisions.md`, "Experiments to run in step 10"): X1 which seasons to train on (2003+, 1994+ only rows with qualifying (10,414 rows), 1994+ with fill and flag, all years), X2 qualifying features yes/no, X3 best of `q1`-`q3` against `q1` only, X4 gap unit and cap, X5 empty against filled qualifying, X6 rank against share of the leader's points, X7 window of the form, X8 `constructorId` against a lineage table. An exploratory run (not evidence) suggested: qualifying adds about +0.02 to +0.03 PR-AUC, dropping 1950-2002 costs nothing, and `q1` only is not distinguishable from the best time.

**Work that is not a decision:**
1. **Step 7 (cleaning) still to do:** apply A1-A4 (typed clean tables; q-times in seconds; dates; keep lists), build the **clean modeling table** (one row per driver-race, with `has_qualifying`), show before/after counts, and the **EDA after cleaning** (the brief requires before and after).
2. **Step 8 (features):** build, leakage-safe (earlier races only: sort by date, group by driver or team, shift by one race before any rolling window): grid, qualifying position and gap (E4), standings before the race (rank and share, F1-F5), the five form windows for driver and team (G1-G5), field size, and whatever G6-G10 decide.
3. **Step 9:** Q1, Q2 (the groundwork and the decision I4 are done; add the figure and written answer), Q3 (each with joins, plot, answer, a short note on grain/missingness/cutoff).
4. **Step 10:** the split, baseline + second statistical model + shallow neural network, the experiments X1-X8, feature-group ablation, two preprocessing-order experiments, permutation importance, SHAP, LIME/local SHAP, the inference function (complete and partially missing record), model comparison table (validation and test, all metrics, intervals by race), D2/D3.
5. **Final:** Restart-and-Run-All, Kaggle upload (path variable, SVG), GitHub push (I do the commits), the PDF report (answers to Q1-Q3 with figures, selected features and why valid pre-race, limitations: qualifying coverage drift, era sensitivity, B1 proxy, sprint, label noise from disqualifications).

**Questions I may send to the teaching assistant** (the brief is ambiguous): three or five metrics; is the introduction's split binding; must the local explanation be LIME; is scikit-learn's MLP an acceptable neural network; what counts as the baseline; may the modeling table cover only 2003+; must `grid = 0` rows be included; how "mechanical retirement" is counted; Q1 years and front-row definition; what "preprocessing-order experiments" means. Defaults for each are already what we do.

---

## PART 8: TIME (this changes how you must work)

We have spent three days taking decisions **one at a time** with detailed evidence. About **2 days** remain and most of the building (clean table, features, Q1-Q3, models, XAI, inference, report, Kaggle, run-all) is **not done**. Therefore:
- **Stop deliberating low-impact decisions one by one.** For the remaining open decisions, present them **in batches of 3-5 with a recommended default and one line of evidence each**, and let me confirm or change the whole batch. Record each in `F1_decisions.md` (short reasoning, no long sections) and add notebook cells only for what the report needs.
- Suggested order: confirm G6-G10, D2, D3, H1-H3, J1-J5 in two or three batches (about an hour); then **build** (step 7 application, step 8 features, Q1-Q3 with plots) and run the step 10 experiments; K1-K6 and L1-L10 should be confirmed as a batch with defaults (split = the introduction's, PR-AUC main, scikit-learn MLP, seed 42, tuning on validation).
- Day plan: **16 Oct** finish decisions and build the clean table and features; **17 Oct** Q1-Q3, split, models, experiments, ablation, XAI, inference function; **18 Oct** report (PDF), Restart-and-Run-All, Kaggle, GitHub, form (before 11:59 PM). Tell me early if something will not fit, and propose what to cut (for example X8, X1 variants, the optional lineage table).
- Teammates can take Q1-Q3 in parallel: offer to write each as an independent notebook section with its own inputs.

---

## PART 9: WHAT I WANT FROM YOU NOW

1. Do Part 1 completely, and run the verification.
2. Reply with: (a) a short summary in your own words of where we are, (b) decisions taken and open, (c) anything in the files that contradicts this prompt or looks wrong, (d) what you would cut or reorder given the 2 days, and (e) any decision already taken that you think is weak, with data.
3. Then ask me to confirm **G6**, and propose the first batch of remaining decisions with defaults (Part 8). Do not edit the notebook, `F1_decisions.md` or git until I answer.
