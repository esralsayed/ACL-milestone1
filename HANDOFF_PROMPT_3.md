# HANDOFF PROMPT 3: continue the F1 podium project (paste this into the new conversation)

You are **Claude Code inside VS Code** on a Windows machine, continuing, as the same assistant, a project that I (the team leader of a university team) have been building with Claude in earlier conversations. Do **not** change anything until you have finished Part 1 and given me the summary in Part 11. Then wait for my answer.

Project folder: `C:\Users\harho\OneDrive\Desktop\ACL 2\VSCode` (git repository, remote `https://github.com/esralsayed/ACL-milestone1.git`, branch `main`).
**Deadline: 18 October 2026, 11:59 PM.** This prompt was written on **17 October 2026: about 1.5 days remain.** Read Part 10 (time) before anything else.

This prompt replaces `HANDOFF_PROMPT.md` and `HANDOFF_PROMPT_2.md` (older; keep them, do not follow them).

---

## PART 1: READ FIRST (in this order, completely)

1. `M1 Desc.pdf` (the brief) and `ACL formula 1 intro.pdf` (the Formula 1 introduction). The Read tool returns nothing useful for PDFs: use `/mingw64/bin/pdftotext -layout "<file>" -` (the PDFs are not UTF-8; symbols shown as "�" are `<=`, `>=` or dashes).
2. **`F1_decisions.md`**: the most important file. Plan (10 steps), the 74 decisions (tables A to M; the last column says what was chosen, `open`, or `Deferred to the modelling phase`), a "Why <ID>" reasoning section per decision with the numbers, the list "Experiments to run in step 10" (X1-X9), and the 33 edge cases. Its tables are padded by my editor, so any script that edits a row must find it with a regex such as `^\| J4\s+\|.*$` and replace the last cell, never an exact string.
3. **`F1_podium_prediction.ipynb`** (**316 cells**, 132 code). Too big for the Read tool: dump it with a short Python script (load the JSON, print each cell's index, type, id and full source) into the scratchpad and read **all** of it.
4. `README.md`, `F1_project_explained.md`, `F1_data_overview.md`, `F1_table_reference.md`, `F1_EERD.md`, the two SVGs, `HANDOFF_PROMPT.md`, `HANDOFF_PROMPT_2.md`: background only (partly superseded; the notebook and `F1_decisions.md` win).
5. `csvs/` (14 tables): look at the first rows of each yourself.
6. `git log --oneline` and `git status`. Last known HEAD: `168dd0e last 2 in J remain` (I commit myself; never commit or push unless I ask).
7. `.venv`: pandas 3.0.6, numpy 2.5.3, matplotlib, seaborn, scikit-learn 1.9.1, scipy, shap 0.52, lime, ipykernel. **Not installed:** statsmodels, PyTorch, TensorFlow, Keras. Run Python as `.venv/Scripts/python.exe` with `PYTHONIOENCODING=utf-8`.
8. Your memory directory has one note: report evidence for **all years (1950-2024) first**, later periods only as labelled extras.

Then verify, and tell me if anything differs: the notebook has 316 cells and ends with the cell "**Result (J3):**"; `F1_decisions.md` has 74 decisions, of which 49 decided, 3 deferred to step 10 (C4, D2, D3) and 22 open (J4, J5, K1-K6, L1-L10, M1-M4); the "Decided so far" line ends with "J1, J2, J3."

---

## PART 2: HOW I WANT YOU TO WORK (read twice; these override politeness)

**Professional standards**
- Work as a professional data analyst, **not as an assistant that agrees with me.** If something I ask is weaker than an alternative, wrong, or hides a risk, say so with the evidence **before** doing it. If I insist, do it my way and state the limitation in the notebook and the md.
- Check soundness every time: leakage (known before the race?), grain (one row per driver per race), missingness, selection bias, era effects, sample size, proof versus proxy.
- **Every number, count, name or year you give me must come from code you ran on the CSV files** (or an output already in the notebook). **Never add up numbers by hand** (in this project I once gave wrong group totals by summing a table in my head; compute every total with code). If you correct an earlier number, say so plainly and fix every place it appears.
- **No outside Formula 1 knowledge as evidence.** If domain knowledge is unavoidable (e.g. the nine nationality links of I1, the meaning of a status word in J1, which team became which), say it is **"not from the data"**. The introduction PDF and the brief are allowed sources: quote them.
- Never refer to a file, column, cell, variable or decision you have not opened and verified.
- **Every team member can be asked about any step, and "an AI tool suggested it" is not accepted.** Every claim needs a number, and I must be able to explain it simply.
- When my words can be read two ways, **state the reading you use** (and ask if it changes the result). Use "they/them" for people whose pronouns are not stated.
- **Give all-years evidence first** (the full cleaned table, 1950-2024), later periods only as labelled extras, unless the question itself fixes the years (Q1 uses 2003-2024 by H2; Q3 uses 2014-2024).

**How we take a decision (the loop)**
1. I say "move to the next decision" (or name one).
2. You **explain first, step by step, in simple English, with real rows and numbers** (I often ask "explain simply" or "from the beginning": use a real example, e.g. one driver or one circuit, and a toy version if useful), and say *why* the decision exists.
3. Options in a table with numbers for each, what each rejected option costs, and **one recommendation**.
4. **Wait for my choice. Record a decision only after I confirm it.** Never present an undecided item as decided.
5. When a decision picks a number (a minimum, a threshold), justify it **by trial and error on the data**: try several values in one notebook cell and show how the answer changes (as in H3 and J4). Do not pick a number by judgement and present it as data-based; if a number is a convention, say so.
6. After I choose: add notebook cells (a markdown cell "how we came to this question", code cells with the evidence, a markdown cell with the result, the decision, the reasons, the rejected options and the limit) **unless I say "md only"**, and always edit `F1_decisions.md`: the row's last cell, the "Decided so far" line, and a "Why <ID>" section placed before the next group heading (J sections go before `### K. Split and evaluation`).

**Phases**
- In cleaning and feature definition **do not fit models and do not choose by predictive score.** Use counts, rates, descriptive statistics. Predictive comparisons are step 10 experiments (X1-X9). Earlier score checks in C1, C2, E5 and F1 are labelled "exploratory, not evidence".
- I decide when something "belongs to the modelling phase" (I did this for D2 and D3): then record it as **Deferred to the modelling phase (step 10)** with the facts and the candidates, not as decided.
- Raw CSV files are immutable; cleaning happens on copies. The notebook assumes no domain knowledge: every claim is first discovered by code in the notebook.

**Style:** simple English, short sentences, tables, real numbers. Do not add complexity I did not ask for (I rejected a sensitivity check for J1: when I say "just take what I told you", do exactly that). Do not commit or push.

---

## PART 3: TECHNICAL GOTCHAS (learned the hard way)

1. **VS Code overwrites notebook edits** if the notebook is open with unsaved changes. Before editing, check the cell count and last cell on disk. After every write, tell me: close the notebook **without saving** (or `File: Revert File`), reopen, check the cell count, then Ctrl+S.
2. **Edit the notebook with a Python script**: load the JSON, `assert` the expected cell count and that the last cell is the one you expect, `assert` the section is not already inserted, append cells with fresh 8-hex-character ids (`secrets.token_hex(4)`), `execution_count: None`, `outputs: []`, `metadata: {}`, write back with `json.dump(nb, f, indent=1, ensure_ascii=False)`. `NotebookEdit` fails on this notebook.
3. **Write scripts and cell sources with the Write tool, never long bash heredocs** (heredocs broke twice in this session: quotes and `\N`). Put cell sources in a `.py` file as raw strings: `CELLS = [("markdown", r'''...'''), ("code", r'''...''')]`. Keep temporary files in the scratchpad directory given in your own system prompt.
4. **Test every new code cell before inserting it** with a harness script (rebuild it in your scratchpad): execute all existing code cells of the notebook in order in one namespace (matplotlib backend `Agg`, `display` replaced by a function that prints `.to_string()`, `plt.show` replaced by a function that saves the figure to PNG for the new cells only, the last expression of each cell evaluated and printed), then the new cells, and **read the output before writing the interpretation**. A full run of the 316 cells takes about 35-50 seconds. **Every number in the notebook text must come from that output.** **Look at every plot as a PNG before describing it** (fix overlaps; e.g. a legend covering data).
5. **Backslash trap:** the placeholder is the two characters `\N`. In Python source use `chr(92) + "N"`; `"\N"` is a syntax error.
6. **pandas 3:** `groupby(...).apply(..., include_groups=False)`; text columns have dtype `str`; all raw tables are loaded as text (`text[...]`), so watch string versus integer keys. **`raceId` is not in date order** (the 2009 races have IDs 1-17): sort by `date` (`races_by_date`), never by `raceId`. Rolling windows: `s.shift(1).rolling(N, min_periods=1)` (G5: use the races available).
7. Check bugs of the "max instead of min" kind: in this session a "first fully covered season" printed 2024 instead of 2003. Sanity-check every printed number against an earlier table.
8. Kaggle: `DATA_DIR = Path("csvs")` and the relative image `F1_relationships.svg` must work on Kaggle (path variable, uploaded file or PNG).
9. New code cells have **no saved outputs** (cells 254 onward were never run in Jupyter). A full Restart-and-Run-All in Jupyter is still to do.

---

## PART 4: THE PROJECT

**Milestone 1: Formula 1 podium prediction.** Kaggle/Ergast data 1950-2024, 14 linked CSV tables in `csvs/`. **Unit:** one driver in one race. **Target:** `positionOrder <= 3`. **Cutoff:** after qualifying, before the race (the race's own result, points, laps, status, pit stops and standings are leakage; earlier races are allowed).

**Brief checklist:** EDA before and after cleaning with plots; clean `\N`, semantic typing (dates, lap times to seconds); exactly one row per `(raceId, driverId)`; primary and foreign keys checked; three data-engineering questions with multi-hop joins, a plot, an answer and a short note on grain, missingness and cutoff (Q1 front row to podium by circuit, before/after 2014, grid vs qualifying; Q2 home advantage controlling for starting position; Q3 mechanical-retirement rate by constructor, 2014-2021 vs 2022-2024); feature selection justified with evidence and a leakage-safe form feature; a justified train/validation/test split (the introduction suggests train <= 2019, validation 2020-2021, test >= 2022); at least two statistical models plus a shallow neural network (1-2 hidden layers), a baseline, at least three distinct modeling attempts; metrics ROC-AUC, PR-AUC, F1 (the deliverables say "all five metrics": add precision and recall), on train/validation and on the unseen test set, thresholds and hyperparameters from train/validation only; feature-group ablation and at least two preprocessing-order experiments; XAI: permutation importance and SHAP (global), LIME and/or local SHAP (local), stating that importance is not causation (brief section 6: "A feature being important to the model is not proof that it causes podium finishes"); an inference function on a complete and a partially missing record; a **PDF report** (Q1-Q3 answers with figures, selected features and why each is valid pre-race, limitations incl. "historical qualifying-coverage drift, era sensitivity"); a run-all notebook. **Submission:** public Kaggle notebook link + GitHub repo link + PDF report via `https://forms.gle/esDxHsvfzffYHVAZ9`.

**Notebook outline (316 cells, cell index of each section):** loading as text (0-4); missing values per table (5-53); formats (54-97); keys and links (98-104); duplicates, B1-B4 (105-155); EDA, 6 analyses + summary (156-183); "Cleaning: which rows stay" C1, C2, C3, C6, C7, "Applying the filters" (184-210); text labels A5 (211-218); home race I1, I2, I5 (219-231); Q2 control I4 (232-238); E6 (239-244); standings F1-F3 (245-252); F4 (253-257); G2 (258-262); G4 (263-265); G5 (266-270); **G7 (271-276)**; **G9 (277-280)**; **Question 1: H1 (281-287), H2 (288-292), H3 (293-297), answer (298-302)**; **Question 3: J1 (303-307), J2 (308-311), J3 (312-315)**. Decisions with md entries but no notebook cells: C4, D2, D3 (deferred), E2, E5, F5, G1, G3, G6, G8, G10.

**Key variables defined by notebook cells** (later cells depend on them; run earlier cells first): `text` (raw tables as strings), `results_one_row` (26,668 rows, after B1), `eda`, `ERA_BINS`/`ERA_LABELS`, `with_q`, `status_name` (statusId → text), **`clean_rows`** (24,652 rows after all row filters; the model table and the source of all form history, G8), `drivers_clean`/`circuits_clean`/`constructors_clean` (A5), `nationality_to_country`, `home`, `races_by_date` and `previous_race` (F1), `rows_f`, `team_standings`, `rows_t`, `form_rows`, `team_races`, `changes`, `history`, **`form_measures`** (G7: per driver-race `podium`, `finished`, `relative_place`, plus last-5 versions), **`circuit_history`** (G9), **`q1`** (Q1 table: results after B1 without Indy 500, 26,287 rows, with `quali_position`, `front_row_grid`, `front_row_quali`, `period`), `race_q`, `season_cov`, **`wilson(k, n)`** (95% Wilson interval, defined in H2 query 3), `q1_recent` (2003+), `circuit_races`, `attempts` (H3 trial table), `q1_rates`, `wide`, **`q3`** (Q3 table: results after B1, 2014-2024, 4,626 rows, with `status`, `period` ("2014-21"/"2022-24"), `finished`, `mechanical` (J1), `positionText`, `start` (J2)), `status_table`, `mapping`, `MECHANICAL`, `NOT_MECHANICAL`, `starts` (q3 rows with `start`), `by_team`. **Names reused by several cells** (do not rely on them): `rows`, `table`, `changed`, `zero`, `started`, `summary`, `season_of`, `starters`.

---

## PART 5: THE DATA PIPELINE (all numbers verified by code)

- Raw: seasons 75, circuits 77, drivers 861, constructors 212, status 139, races 1,125 (1950-2024), results 26,759, qualifying 10,494 (from 1994; every race has qualifying from 2003), sprint_results 360 (18 races, 2021-2024), driver_standings 34,863, constructor_standings 13,391 and constructor_results 12,625 (from 1958), lap_times 589,081, pit_stops 11,371. 14 primary keys and 23 foreign keys valid. `\N` the only placeholder; blank cells only in `qualifying.q2`/`q3`.
- **Rows:** 26,759 → **B1** 26,668 (podium 3,379) → **C1** remove 1,635 `grid = 0` rows → 25,033 → **C2** nothing removed → **C3** remove Indianapolis 500 (381 rows, 35 podiums) → **24,652 rows, 3,344 podiums (13.6%)** → C6, C7 nothing removed.
- From 2003: 8,884 rows, 1,284 podiums, 428 races (every race has exactly 3 podium rows; over all years 1,112 races have 3 and 2 have 4, shared cars of 1951 and 1955).
- `has_qualifying`: 10,407 True, 14,245 False (E2). Split counts with the introduction's split and a 2003+ window: train 6,802 rows (963 podiums), validation 763 (117), test 1,319 (204).

---

## PART 6: DECISIONS (49 decided, 3 deferred, 22 open; details and numbers in `F1_decisions.md`)

| ID | Decision |
|---|---|
| A1-A4 | Missing = `\N` and blank; lap times to seconds; mixed-format time columns not used; keep lists (A4 incomplete for Q2/Q3, which also use `circuits.country`, `drivers.nationality`, `status.status`, `positionText` letter W) |
| A5 | 3 label corrections by dictionary (`'Argentinian '`→`Argentine`, `United States`→`USA`, `&amp;`→`&`) on copies |
| B1-B4 | Keep the lowest `resultId` row of a repeated driver-race pair; grid and team from that row; both sharers of a place keep it; no renumbering |
| C1 | Remove every `grid = 0` row (incl. 72 pit-lane starts 2015-2024, 0 podiums) |
| C2 | Keep rows with a grid slot and 0 laps (966) |
| C3 | Remove the Indianapolis 500 |
| C5 | Each question uses its own rows: **Q1** `results_one_row` without Indy (keeps the 2 qualifying-front-row drivers who started from the pit lane); **Q2** `clean_rows` (needs a grid position to control for it); **Q3** `results_one_row` 2014-2024, starts = not `W` (keeps the 72 pit-lane starts, 8 mechanical). Models: `clean_rows` + training window (C4). Reasons in "Why C5" in the md |
| C6, C7 | Keep disqualified rows; sprint results not used as features |
| D1 | Target `positionOrder <= 3` |
| E1-E6 | No `grid = 0` rows (prediction function: given grid 0 → last slot); qualifying left empty + `has_qualifying`; best of `q1`-`q3` in seconds; gap to the fastest (percent favoured, unit/cap in X4); grid and qualifying position as two feature groups; team = `results.constructorId` |
| F1-F6 | Previous race = latest earlier date (round 1 takes last season's final standings); no standings row = 0 points; team standings empty before 1958; rank and share of the leader's points built, compared in X6; use `position`, not `positionText` |
| G1 | Five windows: last 3, 5, 10 starts, season so far, career (earlier races only, `min_periods=1`) |
| G2-G5 | Driver form and team form as two groups; follow `constructorId` (renames reset); team form = current team; no earlier start = empty |
| **G6** | Decided by experiment X7: last-N and career windows carry over the season boundary, season so far resets; no extra reset versions |
| **G7** | Three measures of earlier races: **podium share**, **relative place** (rank of `positionOrder` among the race's starters ÷ number of starters; ranking needed because 67 rows would exceed 1), **finish rate** (`Finished` or `+n Laps`). Points rejected (raw and normalized: points table changes by era, repeats the place, corr -0.90/-0.93). Same measures for driver and team form |
| **G8** | Form history computed from **`clean_rows` only** (non-starts and the 72 pit-lane starts are not in the history; 314 prediction rows from 2015 reach one race further back) |
| **G9** | No circuit-history feature (61.7% of rows would rest on 0-2 earlier starts at the circuit; 30.3% none; corr 0.64 with career form) |
| **G10** | **Field size** (starters in the race) built as a feature; year and era decided by experiment X9 |
| **H1** | Q1 with **both** front rows (grid 1-2 and qualifying 1-2), side by side |
| **H2** | "Before 2014" = **2003-2013** against 2014-2024 (from 2003 every race has qualifying; earlier seasons would add races unevenly, 17%-71% of a circuit's 1994-2002 races, from lower-converting years) |
| **H3** | A circuit is ranked with **at least 5 races in each period** (14 circuits; trial and error: from 5 on the rank correlation settles) |
| I1-I5 | Nationality→country table of 25 links (9 "not from the data"); dual nationality = home in either; `USA` merged; home effect inside grid bands, Mantel-Haenszel odds ratio **0.93 (0.78-1.07)**; drivers with no circuit country stay as "never home" |
| **J1** | Explicit mapping of the 57 non-finish statuses of 2014-2024: **47 mechanical (416 rows), 10 not** (Collision, Accident, Collision damage, Spun off, Illness, Disqualified, Excluded, Withdrew, Out of fuel, Retired; 385 rows). Wheel, Puncture, Tyre, Undertray, Front/Rear wing, Wheel nut, Damage, Technical, Vibrations, Debris, Seat are mechanical (my decision). **No sensitivity check** (my decision) |
| **J2** | A race start = **`positionText` is not `W`** (withdrawn): 4,598 starts, 401 mechanical (2014-21: 321/3,246 = 9.89%; 2022-24: 80/1,352 = 5.92%). Complete for every row; separates "failed on lap 1" (R) from "failed before the start" (W) |
| **J3** | One team = one `constructorId` (no ID changes at the 2021/2022 boundary; 11 IDs in both periods) |
| **Deferred** | **C4** (seasons to model, X1), **D2** (class weights/resampling), **D3** (top 3 per race or threshold) |

---

## PART 7: EXPERIMENTS FOR STEP 10 (in `F1_decisions.md`)

X1 seasons: (a) 2003+ with qualifying features, (b) 2003+ without (= X2), (c) all years without qualifying features; X3 best of `q1`-`q3` vs `q1` only; X4 gap unit and cap; **X5 dropped** (only 21 rows from 2003 lack qualifying); X6 rank vs share of leader's points; X7 form window (and G6); X8 lineage table (optional, cut first); **X9 year/era: (a) field size only, (b) + era categories, (c) + year number** (read on validation: the test era 2022-24 has 0 training rows under the introduction's split). Plus D2 and D3, the feature-group ablation (groups: grid, qualifying, standings, driver form, team form, field size) and two preprocessing-order experiments.

---

## PART 8: EDGE CASES

The 33 edge cases are in `F1_decisions.md` ("Edge Cases to Handle", some counts are raw, before B1). Found in this session, add them to that table when convenient:
- `positionOrder` still counts rows removed by C1, so `positionOrder / starters` exceeds 1 in 67 rows (52 races): G7 ranks among the starters first.
- The 72 pit-lane starts (`grid = 0`, laps > 0) are real races but not in `clean_rows` (C1, G8); Q3 counts them (J2).
- `laps = 0` cannot tell "failed on lap 1" from "failed before the start": `positionText` R/W can (J2). 28 W rows in 2014-2024, 15 with a mechanical status; Räikkönen 2017 Malaysia is R with grid 0 and 0 laps.
- Sprint weekends 2021-2023: 7 of the 38 rows that qualified on the front row but did not start there (the sprint can set the Sunday grid, C7).
- Some races have only one grid front-row starter in the table (e.g. Interlagos 2014-24: 19 front-row starts in 10 races).
- Same venue under two circuit IDs (Zeltweg/Red Bull Ring 2.2 km, the two Las Vegas circuits 0.2 km, Montjuïc/Pedralbes 3.9 km): none falls inside 2003-2024 with two IDs.
- Constructor IDs: Sauber's ID 15 covers 2014-2018 and again 2024; renames inside the Q3 periods split teams into pieces of 44-48 starts; timing pairs are ambiguous (Force India pairs with Racing Point and Alfa Romeo).
- Status labelling shifts between Q3 periods: Collision damage 5.3% of non-finishes in 2014-21, 13.9% in 2022-24; Brakes 7.4% and 2.1%. `Retired` (no reason) is 6.3% / 6.2%.
- Seasons 2014-2024 have 17 (2020) to 24 (2024) races; Caterham (33 starts) and Marussia (31) raced part of 2014 only.

---

## PART 9: WHAT IS LEFT

**J4 (in progress, not confirmed):** minimum starts for a team to be ranked in Q3. My recommendation: **B, at least 34 starts in the period** (one full season with two cars in the shortest season: 17 races × 2). Evidence already computed (put it in the notebook after I confirm): per-team rates with Wilson ranges, races per season 2014-2024 (17-24), trial top 3 under minimums 0/34-75/80/100: 2014-21 top 3 with 34-75 = Lotus F1 20.0% (75 starts), Toro Rosso 16.5%, Renault 14.6% (Caterham 21.2% from 33 starts tops it with no minimum); 2022-24 = Alfa Romeo 12.5%, Alpine 10.4%, AlphaTauri 8.0% for any minimum up to 88. Ask me to confirm.

**J5:** count sprint failures in Q3? (raw `sprint_results`: 360 rows, Finished 340, Retired 10, Accident 3, Collision damage 3, Vibrations 1, Electrical 1, Brakes 1, Exhaust 1; recompute by period with the J1 mapping and the J2 start rule.) Then **answer Q3**: table of rates with ranges per team and period, a plot like Q1's, the answer, the grain/missingness/cutoff note, limits.

**Q2:** I4 is done; add the figure (home vs away podium rate inside the grid bands) and the written answer.

**Step 7 (cleaning) to do:** apply A1-A4 (typed clean tables, q-times in seconds, dates), build the clean modeling table (one row per driver-race, `has_qualifying`), before/after counts, **EDA after cleaning** with plots (the brief requires before and after).

**Step 8 (features):** leakage-safe (earlier races only: sort by date, group by driver or team, shift by one race): grid; qualifying position and gap (E4, both units); standings before the race (rank and share, F1-F5); the five form windows × three measures (G7) for driver (from `clean_rows`, G8) and team (current team, all its cars); field size (G10); `has_qualifying`.

**Step 10:** decisions K1-K6 (split; recommended the introduction's split with bootstrap intervals by race, PR-AUC main, ROC-AUC second, threshold on validation, add precision and recall, retrain on train+validation optional, 2020 normal), L1-L10 (fill learned on train, scaling, IDs dropped, two preprocessing orders, logistic regression baseline, gradient boosting or random forest, scikit-learn `MLPClassifier` with 1-2 hidden layers, tuning on validation, ablation groups, seed 42), M1-M4 (explain the best model, one local example, dictionary input, a record with no qualifying); D2, D3; experiments X1-X9; ablation; XAI; inference function; model comparison table (validation and test, five metrics, intervals by race).

**Final:** Restart-and-Run-All (check time), Kaggle upload (path variable, SVG), GitHub (I commit), PDF report, submission form.

**Questions I may send to the teaching assistant:** three or five metrics; is the introduction's split binding; LIME required; is scikit-learn's MLP acceptable; what counts as the baseline; may the model table cover only 2003+; how "mechanical retirement" is counted; what "preprocessing-order experiments" means. Our defaults are already what we do.

---

## PART 10: TIME (this changes how you must work)

About **1.5 days** remain and the build (clean table, features, models, XAI, inference, report, Kaggle, run-all) has **not started**. Therefore:
- Finish J4 and J5 and the Q3 answer quickly (data already computed for J4), then Q2's figure and answer (short).
- Then **build**: step 7 and step 8 first (the models need them), then K/L/M **as one batch with defaults** (I confirm or change the batch), then the models and the experiments.
- Tell me early what will not fit and propose cuts, in this order: X8, X3, X4 cap, X9 variant (c), some X7 windows, LIME (keep local SHAP). Never cut a brief requirement (three models incl. NN, baseline, five metrics on validation and test, ablation, two preprocessing orders, permutation importance + SHAP + one local explanation, inference function on complete and partial record, report, run-all).
- Teammates can take sections in parallel (Q2 answer, the report, Kaggle): offer self-contained cells or text.

---

## PART 11: WHAT I WANT FROM YOU NOW

1. Do Part 1 completely, and run the verification.
2. Reply with: (a) a short summary in your own words of where we are, (b) decisions taken, deferred and open, (c) anything in the files that contradicts this prompt or looks wrong, (d) what you would cut or reorder given the time, (e) any decision already taken that you think is weak, with data.
3. Then ask me to confirm **J4** (recommendation B, 34 starts) and propose **J5** with data. Do not edit the notebook, `F1_decisions.md` or git until I answer.
