# HANDOFF PROMPT 3 (updated 19 October 2026, after the full notebook run of 00:15): continue the F1 podium project (paste this into the new conversation)

You are **Claude Code inside VS Code** on a Windows machine, continuing, as the same assistant, a project that our university team has been building with Claude in earlier conversations. **Several team members work on the same files** (git authors so far: Hoor Sobh and esraa; other members work on their own copies), so always check `git log`, `git status` and what is on disk before you trust anything, including this prompt. Do **not** change anything until you have finished Part 1 and given the summary in Part 12. Then wait for an answer.

Project folder: the repo is cloned on more than one machine. Known paths: `C:\Users\harho\OneDrive\Desktop\ACL 2\VSCode` and `C:\Users\ALRWOAD LAPTOP\Desktop\Sem 9\ACL\ACL-milestone1`. Use the folder you are started in. Git remote `https://github.com/esralsayed/ACL-milestone1.git`, branch `main`.

**Where we are in one paragraph:** every part of the brief that lives in the notebook is built: audit, cleaning, EDA before **and after** cleaning, Q1-Q3, features, split, metrics, four models, tuning, ablation, the two preprocessing-order experiments, the final comparison on the test seasons, the explanations (XAI) and the prediction function. **All 74 decisions are taken** (none open, none deferred). The whole notebook was run in order in VS Code with no errors. What is left is tidying old text, a fresh Restart-and-Run-All, and the deliverables outside the notebook (PDF report, Kaggle, GitHub, submission form). Read Part 11 (time) first: the brief's deadline (18 October 2026, 11:59 PM) had passed when this prompt was written.

This prompt replaces `HANDOFF_PROMPT.md`, `HANDOFF_PROMPT_2.md` and the earlier versions of this file (in git history).

---

## PART 1: READ FIRST

1. `M1 Desc.pdf` (the brief) and `ACL formula 1 intro.pdf` (the introduction). Use `/mingw64/bin/pdftotext -layout "<file>" -` (not UTF-8; "�" is `<=`, `>=` or a dash).
2. **`F1_decisions.md`** (about 1,620 lines): plan, 74 decisions in tables A-M (last column = what was chosen), a "Why <ID>" section per decision with the numbers, experiments X1-X9, the "Final comparison" section, 33 edge cases. Its tables are padded: edit a row with a regex such as `^\| M1\s+\|.*$` and replace the last cell.
3. **`F1_podium_prediction.ipynb`** (**481 cells**, 216 code). Dump it with a Python script (index, type, number of outputs, full source, outputs) into the scratchpad and read all of it, at least cells 340-480 in full.
4. Background only: `README.md`, `F1_project_explained.md`, `F1_data_overview.md`, `F1_table_reference.md`, `F1_EERD.md`, the two SVGs, the older handoff prompts, `prev_chat.md` (the earlier chat with the X6/X7/X9 results that the notebook now reproduces).
5. `git log --oneline` and `git status`. Last known HEAD: `04e934d explainability remains` (Hoor Sobh). **When this prompt was written, the notebook, `F1_decisions.md`, this file and `prev_chat.md` were staged (`git add`) but not committed.** The team commits; never commit or push unless asked.
6. **Python.** The last run used the kernel "Python 3" = system Python **3.11.9** on the `ALRWOAD LAPTOP` machine: pandas 3.0.0, numpy 2.4.1, **scikit-learn 1.8.0**, scipy 1.17.1, matplotlib 3.10.8, seaborn 0.13.2, **shap 0.51.0**, lime, jupyter_client, ipykernel (no `.venv` in that folder). An earlier run used a `.venv` (Python 3.13.5, scikit-learn 1.9.1, shap 0.52) on another machine. **Gradient boosting gives slightly different numbers between the two scikit-learn versions** (tuned model: 0.721 with 1.8.0, 0.715 with 1.9.1); logistic regression, random forest and the network give identical numbers. Check which Python you have and say so. (With `python -I`, `PYTHONIOENCODING` is ignored: use `python -I -X utf8`.)
7. Memory note: report evidence for **all years (1950-2024) first**, later periods only as labelled extras.

**Verify, and report anything that differs:**
- Notebook: 481 cells; the last one is the markdown "**Result (the prediction function):**".
- **Saved run:** all 216 code cells ran **in cell order in one go** (execution counts 224-439, contiguous), **no error outputs**; every code cell has output except 1, 6 and 55 (they only define things). The kernel was **not restarted** before that run (counts do not start at 1), so a fresh Restart-and-Run-All is still to be shown (Kaggle will do one anyway).
- Spot checks of the saved outputs: tuned models on validation 0.706 / 0.725 / 0.721 / 0.741 (logistic regression / random forest / gradient boosting / network); career form 0.740 / 0.744 / 0.733 / 0.750; X7 rolling check "2 of 4" models above 0; final thresholds 0.287 / 0.384 / 0.319 / 0.406; test PR-AUC 0.666 / 0.716 / 0.717 / 0.722; prediction function 0.819 (complete) and 0.068 (partial).
- `F1_decisions.md`: "Decided so far" ends with "..., L10, D2, M1, M2, M3, M4."; no row says `open`.

---

## PART 2: HOW WE WORK (these override politeness)

**Professional standards**
- Act as a professional data analyst, not an assistant who agrees. If a request is weaker than an alternative, wrong, or hides a risk, say so with evidence **before** doing it; if the team insists, do it and state the limitation in the notebook and the md.
- Check every step for leakage (known before the race?), grain (one row per driver per race), missingness, selection bias, era effects, sample size, proof versus proxy.
- **Every number, count, name or year must come from code you ran on the CSV files or from a saved notebook output. Never add up numbers by hand.** If you correct a number, say so and fix every place it appears.
- **No outside Formula 1 knowledge as evidence.** If unavoidable (the 9 nationality links of I1, the meaning of a status word in J1), label it **"not from the data"**. The introduction and the brief are allowed sources: quote them.
- Never refer to a file, column, cell, variable or decision you have not opened.
- Every team member can be asked about any step, and "an AI tool suggested it" is not accepted: every claim needs a number and a simple explanation.
- When a request can be read two ways, **state the reading you use**. Use "they/them" for people whose pronouns are not stated.
- **The user wants simple explanations** (often "like to a 5-year-old"): short sentences, a real example (one driver, one race), tables. Explain every renamed column by its original column (e.g. `rank_before` = `position` of `driver_standings` at the previous race).

**The decision loop**
1. The team names the decision. 2. Explain step by step in simple English with **real rows and numbers**. 3. Options table with numbers, the cost of each rejected option, **one recommendation**. 4. **Wait for the choice; record only after it is confirmed.** 5. When a decision picks a number, justify it **by trial and error on the data** (several values in one cell); if a number is a convention, say so. **Fix the decision rule before running an experiment** (we used: "keep the current choice unless the other is better beyond chance, i.e. its whole 95% range above 0, in at least 2 of the 4 models"; ranges read at three decimals, so +0.000 counts as touching 0). 6. Then add notebook cells (markdown "How we came to this question", code with the evidence, markdown "Result" + "Decision" + reasons + rejected options + limits) and always edit `F1_decisions.md` (the row, the "Decided so far" line, a "Why <ID>" section).

**Phases**
- Choices were made **on validation 2020-2021 only** (plus the rolling check 2018-2021), with PR-AUC (primary, K2) and its 95% range from resampled races (`race_samples`).
- **The test seasons 2022-2024 were used once, in the final comparison; nothing was chosen from them.** Explanations (XAI) and the prediction-function demo use test rows, which is allowed because they fit and change nothing. **Do not tune, select features or change thresholds now** (that would spoil the test); if the team asks, explain why (the notebook cell "Why every choice was made on validation" does this) and record any change as a limitation, not as an improvement.
- Raw CSVs are immutable. The notebook assumes no domain knowledge: every claim is discovered by code first.

**Style:** simple English, short sentences, tables, real numbers. No complexity that was not asked for. The team removed two things on purpose; do not bring them back: the "last 5 + career" variant of X7 and the experiment X10 (within-race comparison features). Do not commit or push.

---

## PART 3: TECHNICAL GOTCHAS

1. **VS Code overwrites notebook edits.** This happened several times: the user saved an open notebook and our file edits were lost (once the X10 removal, once the column-name notes). Before every write: check the cell count, the last cell and a marker of the previous edit on disk. After every write tell the user: **`File: Revert File`** (or close without saving and reopen) **before saving**. After the user says they saved, re-check that the earlier edits survived.
2. **Edit the notebook with a Python script:** load the JSON, `assert` the expected count and the text of the neighbouring cells, `assert` the new section is not already there, insert cells with fresh ids (`secrets.token_hex(4)`), `execution_count: None`, `outputs: []`, `metadata: {}`; write with `json.dump(nb, f, indent=1, ensure_ascii=False)`. `NotebookEdit` fails on this notebook.
3. **Write scripts and cell sources with the Write tool**, cell sources as raw strings in a `.py` file: `CELLS = [("markdown", r'''...'''), ("code", r'''...''')]`. Temporary files go in your scratchpad directory.
4. **Testing new cells quickly: a persistent Jupyter kernel.** A full run takes several minutes (about 6.5 min up to the old cell 414; more now with SHAP on 1,319 rows). Start a kernel in the project folder in the background: `MPLBACKEND=Agg PYTHONIOENCODING=utf-8 python -m ipykernel_launcher -f <scratch>/conn.json`, then send code with a small `jupyter_client.BlockingKernelClient` script (run notebook cells i..j quietly, or a `.py` file / `CELLS` list loudly). Run all existing cells once, then test only the new ones. To look at plots, patch `plt.show` in the kernel to `savefig` into the scratchpad and read the PNG. **Always re-test new cells from the notebook file in notebook order**, with later variables deleted: once an L4 cell used `final_pred`, which only exists in the later final comparison; it passed in the kernel but would have failed in a Run-All (fixed: it uses `l9f_pred`).
5. `\N` in Python source: `chr(92) + "N"`.
6. pandas 3: `groupby(...).apply(..., include_groups=False)`; raw tables are text (`text[...]`). **`raceId` is not in date order**: sort by `date`. Windows: `s.shift(1).rolling(N, min_periods=1)` / `s.shift(1).expanding()`.
7. Sanity-check printed numbers (a `max`/`min` slip once printed 2024 instead of 2003).
8. **Names redefined by later cells** (the last definition wins in a Run-All): `best_f1_threshold` (cell 356 returns `(threshold, best F1)`, cell 360 the threshold only; later cells use the 360 version), `BASE_FEATURES` (341: with `field_size`; 386: `base_podium_chance` instead), `QUALI_FEATURES` (341: position, gap, flag; 372: position and flag), `FEATURES_L1` (366, 372, 386; the last-5 names), **`FEATURES_FINAL`** (444; the same 16 features with the career names, used by everything after X7), `rng` (240, 305, 342, 415), **`predict_podium`** (469: a short helper of the XAI section; 477: the prediction function), and many short names (`rows`, `summary`, `before`, `after`, `d`, `p`, `m`, `trn`, `val`, `samples`, `colors`, `order`, `low`, `high`...).
9. **Which features each result used:** X1, K2-K6, K3/D3 and L1: with the qualifying gap and field size. L5-L7: the 16 features with last-5 form, untuned. L8, L10, D2, L9, X6, X9: 16 features, last-5 form, tuned. X7 onward (career switch, L9 on career, L4, final comparison, XAI, prediction function): 16 features with **career** form, tuned (option B2).
10. Kaggle: `DATA_DIR = Path("csvs")` and the relative image `F1_relationships.svg` must work there (path variable, uploaded file or PNG).

---

## PART 4: THE PROJECT

**Milestone 1: Formula 1 podium prediction.** Kaggle/Ergast data 1950-2024, 14 CSV tables in `csvs/`. **Unit:** one driver in one race. **Target:** `positionOrder <= 3`. **Cutoff:** after qualifying, before the race.

**Brief checklist, with where each item is:**
| Requirement | Status / where |
|---|---|
| EDA before cleaning, with plots | done: "Exploring the Data (EDA)", 6 analyses |
| EDA after cleaning ("impact of the cleaning") | **done:** "EDA after cleaning: what the cleaning changed" (cells 211-215) |
| `\N` cleaned, semantic typing (dates, lap times in seconds) | done in the audit and feature cells (A1, A2; `races_by_date`, `lap_seconds`); **no short visible summary cell yet** (optional, Part 10) |
| One row per `(raceId, driverId)`; keys checked | done (B1-B4; keys) |
| Q1-Q3: multi-hop joins, plot, answer, grain/missingness/cutoff | done (three answer sections) |
| Features justified with evidence; "plotting the effect of the features" | done (E, F, G sections; "The 16 features and how each relates to the podium") |
| Effect of a step on distribution/range/values | done (L2 figure; L4 build cells; EDA after cleaning) |
| A justified split | done (K1) |
| Baseline + 2 statistical models + shallow network; 3+ modelling attempts | done (L5-L8) |
| ROC-AUC, PR-AUC, F1 (+ precision, recall) on train/validation **and** test | done: "Final comparison" |
| Thresholds and settings from train/validation only | done (K3, L8; test never used for a choice) |
| Feature-group ablation | done (L9, and L9 on the career form, with all metrics per run) |
| At least two preprocessing-order experiments | done: "L4: the two preprocessing-order experiments" |
| XAI: permutation importance + SHAP (global); LIME and/or local SHAP (local); "not causal" | done: "Explaining the model (XAI)" |
| Inference function on a complete and a partially missing record | done: "The prediction function (inference)" |
| Run-all notebook | run in order without errors; fresh restart still to show |
| **PDF report**, **Kaggle** public notebook, **GitHub** repo, **submission form** `https://forms.gle/esDxHsvfzffYHVAZ9` | **not done** (team) |

**Notebook outline (481 cells; first cell of each section):** title 0; tables 4; missing values 5; formats 54; keys 98; duplicates B1-B4 105; EDA before cleaning 156; row filters C1 185, C2 189, C3 193, C6 197, C7 203; applying the filters 209; **EDA after cleaning 211**; labels A5 216; home race I1/I2/I5 224; Q2 control I4 237; Q2 answer 244; E6 248; standings F1-F3 254; F4 262; G2 267; G4 272; G5 275; G7 280; G9 286; **Q1** H1 290, H2 297, H3 302, answer 307; **Q3** J1 312, J2 317, J3 321, J4 325, J5 331, answer 335; **modelling:** K1/C4/X1 340, rolling check 347, K2 351, K4-K6 354, K3/D3 359, L1 362, E4 revisited 370, L2 374, L3 379, L4 plan 382, G10 updated 385, the 16 features 388, L5 392 (+ follow-up 395), L6 398, L7 401, L8 404, L10 411, D2 414, L9 417 (all metrics per run 420); **X6/X9/X7 423** (X6 425, Spearman 429, X9 432, X7 435); **career switch 443**; **L9 on career 445**; **L4 experiments 451**; **final comparison 458** (why validation, not test: 459); **XAI 466**; **prediction function 475** (why these choices: 476).

**Key variables (cleaning and questions):** `text`, `results_one_row` (26,668), `eda`, `status_name`, **`clean_rows`** (24,652), `drivers_clean` / `circuits_clean` / `constructors_clean`, `q1`, `q2`, `home`, `q3`, `races_by_date`, `previous_race`, `rows_f` (`rank_before`, `points_before`), `rows_t` (`team_rank_before`, `team_points_before`, `state`), `form_measures`, `wilson(k, n)`, `MIN_STARTS` (34).
**Modelling variables:** `x1_table`, `l1` (unfilled model table), `fill_empty(rows, train_rows)` (L1), `l1_filled` / `l1_trn` / `l1_val` and `tree_trn` / `tree_val` (last-5 form), `race_samples(rows, n=1000, seed=42)`, `y_val`, `fast_pr_auc(y, p)`, `L9_MAKERS` (the four tuned seed-42 model builders), `L8_BEST`, `l9_pred`, `l9_samples`; X section helpers `x_frames(base, train_end, extra)`, `x_predict`, `x_compare`, tables `x6`, `x7`, `x9`, `window_table(w)`, `rolling_rows`, `roll_pred`; **career form (final):** `career_base`, `CAREER_NAMES`, **`final_filled` / `final_trn` / `final_val`** (filled, for logistic regression and the network) and **`final_tree` / `final_tree_trn` / `final_tree_val`** (empty values left, for the trees), `FEATURES_FINAL`, `DRIVER_FORM_FINAL`, `TEAM_FORM_FINAL`, `l9f_pred`; L4: `exp2_A_trn` / `exp2_A_val` / `exp2_B_trn` / `exp2_B_val`, `exp3_B_trn` / `exp3_B_val` / `exp3_B_tree_trn` / `exp3_B_tree_val`; final comparison: `final_test`, `final_tree_test`, `SETS`, `final_models`, `final_pred[(model, set)]`, `final_threshold`; XAI: `xai_model`, `shap_explainer`, `shap_test`, `xai_cases`, `local_shap`, `lime_tables`; prediction function: `predict_podium(record)` (477), `record_from_table(i)`, `FILL_MEDIANS`, `RECORD_KEYS`.

---

## PART 5: THE DATA (all verified by code)

- Raw: races 1,125 (1950-2024), results 26,759, qualifying 10,494 (from 1994; every race has it from 2003), sprint_results 360 (18 sprints, 2021-2024), driver_standings 34,863, constructor_standings 13,391 (from 1958). 14 primary keys, 23 foreign keys valid.
- Rows: 26,759 → B1 26,668 → C1 (−1,635 `grid = 0`) → C3 (−381 Indianapolis 500) → **24,652 rows, 3,344 podiums (13.6%)**, 1,114 races; 1,112 races with exactly 3 podium rows, 2 with 4 (shared cars of 1951 and 1955).
- **Split (K1):** training 1950-2019 (22,570 rows, 13.4% podiums), validation 2020-2021 (763 rows, 39 races, 117 podiums, 15.3%), test 2022-2024 (1,319 rows, 68 races, 204 podiums, 15.5%). A validation PR-AUC has a 95% range about 0.24 wide. Rolling check 2018-2021: 81 races, 1,590 rows, 243 podiums.

---

## PART 6: DECISIONS (all 74 decided; numbers in the md)

| ID | Decision |
|---|---|
| A1-A5 | `\N` and blank = missing; lap times in seconds; mixed-format columns not used; keep lists; 3 label corrections |
| B1-B4 | Lowest `resultId` row per driver-race; grid/team from it; sharers both keep a place; no renumbering |
| C1-C3, C6, C7 | Remove `grid = 0` (1,635); keep grid slot + 0 laps; remove Indianapolis 500; keep disqualified; sprints not features |
| C4 | By X1: train on all seasons 1950-2019 with the qualifying features (empty + `has_qualifying`) |
| C5 | Q1-Q3 start from `results_one_row` without the Indianapolis 500; models use `clean_rows` |
| D1 / D2 / D3 | Target `positionOrder <= 3` / **no class fix** (the validation threshold handles the rarity; fixes doubled the probabilities) / predictions not forced to 3 per race, "top 3 per race" reported as an extra F1 |
| E1-E6 | No `grid = 0` rows; qualifying empty + `has_qualifying`; grid and qualifying position as two groups; **qualifying gap removed** (E4 revisited); team = `results.constructorId` |
| F1-F6 | Previous race by date; no standings row = 0 points; team standings empty before 1958; **F5 by X6: rank** (`position`), not the share of the leader's points |
| G1-G10 | **G1 by X7: the career window** (all earlier starts) for driver **and** team form; G6 by X7: carry over; podium share + relative place + finish rate (G7); history from `clean_rows` (G8); no circuit history (G9); **G10: `base_podium_chance` = 3 ÷ starters, no year or era (X9)** |
| H1-H3 | Q1: both front rows; 2003-13 against 2014-24; at least 5 races per period (14 circuits) |
| I1-I5 | Q2: 25 nationality links (9 "not from the data"); dual = either; grid bands + Mantel-Haenszel; "never home" rows stay |
| J1-J5 | Q3: 47 mechanical statuses; start = not `W`; one team = one `constructorId`; ranked with at least 34 starts; sprint failures not counted |
| K1-K6 | The introduction's split; PR-AUC primary, ROC-AUC secondary; **best-F1 threshold per model on validation, used unchanged on test (final: 0.287 / 0.384 / 0.319 / 0.406)**; ROC-AUC, PR-AUC, F1, precision, recall (no accuracy); no retraining on train + validation; 2020 a normal season |
| L1-L3 | Fill + flag for logistic regression and the network (qualifying = grid, empty rank = last place, form = training median), no fill for the trees; standard scaling on training rows; IDs not model inputs |
| L4 | Two preprocessing-order experiments (fill↔scale; filter↔form). **Run: both of our orders stay** |
| L5-L7 | Baseline = logistic regression on all features; random forest **and** gradient boosting; scikit-learn `MLPClassifier`, 1-2 hidden layers |
| L8 | Small grid search on validation: logistic regression C = 0.1; random forest leaves ≥ 50, sqrt, 300 trees; gradient boosting learning rate 0.1, 15 leaves, leaves ≥ 50; network 32 + 16, alpha 0.0001 (tuned on last-5 form; kept after X7, option B2) |
| L9 | Six feature groups removed one at a time + grid & qualifying together; **feature set unchanged** (last 5 and career: only grid + qualifying together clearly matters) |
| L10 | Seed 42 for every model with randomness (the network's seed 42 is its best of 5 on validation) |
| **M1** | **Explain the neural network** (team's choice: highest PR-AUC on validation 0.750 and test 0.722; within chance of the forest and boosting) |
| **M2** | **Two test rows picked by a rule:** the most confident real podium (Verstappen, 2022 Canadian GP, 0.819) and the real podium rated lowest (Gasly, 2024 São Paulo GP, 0.004); local SHAP (waterfall) and LIME |
| **M3** | **The prediction function takes a dictionary** (model-table names; missing = left out or `None`; `grid` and `starters` required) |
| **M4** | **Partial record = a debut without qualifying:** Bearman, 2024 Saudi Arabian GP (no rank, no career form), qualifying removed |

---

## PART 7: EXPERIMENTS (all done)

| # | Result |
|---|---|
| X1 | Variant (d): all seasons from 1950 with the qualifying features |
| X2 | Covered by X1 and L9 |
| X3, X4, X5 | Dropped (gap removed; X5 for time) |
| X6 | **Rank kept:** share of the leader's points says the same (Spearman −0.924); share / both within chance. The notebook also explains Spearman against Pearson (Pearson −0.687 because the relation is curved) |
| X7 | **Career window:** highest in all four models on 2020-21 (+0.009 to +0.033, within chance); rolling check 2018-21 (rule fixed before): career − last 5 = +0.030 (LR) and +0.024 (network) beyond chance, forest +0.021 borderline → rule met (2 of 4). Applied with **option B2** |
| X8 | Mentioned in an old handoff, never defined in the md: treated as dropped |
| X9 | **Base podium chance only:** era within chance and impossible for the test era (no training rows); year −0.041 for the network (beyond chance) |
| L4 exp. 2 | Scale → fill instead of fill → scale: logistic regression +0.000, network −0.014 (within chance) → **ours stays** |
| L4 exp. 3 | Form built from all result rows (non-starts count as worst) instead of real starts only: 40.9% of training rows change their career form; models +0.001 / −0.005 / +0.010 / −0.008 (within chance) → **ours stays** |
| L9 on career | Only grid + qualifying together clearly helps (−0.078 to −0.104); grid alone and team form beyond chance for the network only; feature set unchanged |
| D2, L8, L10 | Done (see Part 6) |

---

## PART 8: FINAL RESULTS (for the report)

**Final comparison** (models trained once on 1950-2019, career form, tuned, seed 42; thresholds from validation; gradient boosting from scikit-learn 1.8.0):

| Test 2022-2024 (68 races, 204 podiums) | PR-AUC (95% range) | ROC-AUC | F1 | Precision | Recall | F1 top 3 per race |
|---|---|---|---|---|---|---|
| Logistic regression (baseline) | 0.666 (0.608-0.734) | 0.929 | 0.657 | 0.554 | 0.809 | 0.632 |
| Random forest | 0.716 (0.658-0.777) | 0.939 | 0.676 | 0.657 | 0.696 | 0.667 |
| Gradient boosting | 0.717 (0.659-0.775) | 0.938 | 0.678 | 0.619 | 0.750 | 0.642 |
| Neural network | 0.722 (0.669-0.778) | 0.936 | 0.668 | 0.656 | 0.681 | 0.662 |
| Grid ranking (reference) | 0.647 (0.591-0.709) | 0.911 | 0.649 | 0.650 | 0.647 | 0.652 |
| Random guess (reference) | 0.155 | 0.500 | | | | |

Validation PR-AUC 0.740 / 0.744 / 0.733 / 0.750 (grid 0.639). The forest, boosting and the network beat the grid ranking (+0.069 to +0.075) and the baseline (+0.050 to +0.056) beyond chance on test; the baseline falls most from validation to test. **Honest note** (in the notebook and md): the exploratory cells of C1/C2 had scored the grid ranking alone on the test years during cleaning (ROC-AUC 0.911, PR-AUC 0.647); nothing was chosen with it.

**XAI (network, test seasons):** permutation importance: grid 0.191, qualifying 0.113, grid + qualifying together 0.380 PR-AUC drop; SHAP beeswarm: grid and qualifying the largest pushes, then career form and team rank (a high career finish rate pushes down: a model pattern from overlapping features, not a cause). Local: Verstappen (grid 1) every main feature pushes up; Gasly (grid 13, 0.004) every main feature pushes down a little: nothing pre-race pointed to a podium. LIME with the 0/1 flags fixed and sampling around the driver (fidelity R² 0.86 / 0.39, chosen against the default's 0.42 / 0.10) agrees with SHAP. **Importance is not causation** is stated explicitly.

**Prediction function:** Verstappen 2022 Canada (complete) 0.819 = the model's own prediction; Bearman 2024 Saudi Arabia (real debut) 0.134 = the model's own prediction; without qualifying 0.068. **Limit:** the drop comes only from `has_qualifying` = 0 (in training a missing qualifying meant a season before 1994).

**Limitations to put in the report:** 39 validation races (differences under about 0.03 not separable); one seed (the network's is its luckiest); gradient boosting depends on the scikit-learn version; qualifying coverage drift (none before 1994, patchy until 2002) handled by `has_qualifying` + the fill; era sensitivity (the test era has no training rows); 72 pit-lane starts not in the model table; L8/L10/D2 chosen on last-5 form (option B2); "preprocessing order" is our reading of the brief.

---

## PART 9: EDGE CASES, INCONSISTENCIES, AND THE TIDY LIST

**Edge cases** found later and not yet in the md table: `positionOrder` still counts rows removed by C1 (67 rows would have relative place above 1); the 72 pit-lane starts are real races but not in `clean_rows` and are counted in Q3; `laps = 0` cannot separate "failed on lap 1" (R) from "failed before the start" (W); Räikkönen 2017 Malaysia is R with grid 0 and 0 laps; 7 of the 38 qualifying-front-row drivers who did not start there are sprint weekends; Sauber's ID 15 covers 2014-2018 and 2024; a sprint row has the letter `N`; 1,553 training rows have no standings rank (615 first starts); 23 rows (round 1 of 1950) have no previous standings at all.

**The tidy list (the next step, agreed with the user: done after the run, now possible):**
1. **Gradient-boosting numbers in the text** come from the earlier `.venv` run (e.g. 0.715 tuned, 0.713 untuned) while the saved outputs show scikit-learn 1.8.0 numbers (0.721, 0.716). Markdown cells quoting the old ones: 400, 410, 413, 416, 422, 439, 449 (cell 423 quotes both on purpose, as the version note). Decide with the team: update the text to the saved outputs (recommended, so text and outputs agree) and say so in the md.
2. **Notes written before later decisions:** cell 266 (F4: "this still has to be confirmed"), 346 (X1: "checked again when the step-8 features are complete"), 394 (L5: "refitted ... after step 8"), 397 (L5 follow-up: "the remaining step-8 features"), 404 (L8: "L10 open", "D2 open"), 409 (L8 code comment: "L10 open").
3. **The name clash** `predict_podium` (469 helper vs 477 function): rename the XAI helper (e.g. `net_probability`) and re-test 469-473.
4. **md:** the plan table still says steps 7, 8, 10 "To do"; in "Why L1" the "Update" paragraph splits the table; the "Decided so far" line leaves out C5; the C4 row describes a median fill that L1 replaced; the experiments table has no X8 row.
5. Optional: a short visible "semantic typing" summary (dates via `races_by_date`, lap times via `lap_seconds`) for the brief's checklist.

---

## PART 10: WHAT IS LEFT (in the order we agreed)

1. **Tidy the old text** (Part 9 list), re-test the edited cells.
2. **Fresh Restart-and-Run-All** in VS Code (Restart Kernel, then Run All; it takes several minutes), check no errors, save. The user runs it; afterwards re-check the file (Part 3.1).
3. **Kaggle:** public notebook with the data (`csvs/`) and the SVG; check that the paths work there.
4. **PDF report** (teammates can start in parallel; offer text and figures): Q1-Q3 answers with figures; the selected features and why each is known before the race; the model results (Part 8); the explanations ("importance is not causation"); the limitations.
5. **GitHub:** the team commits and pushes (never commit unless asked).
6. **Submission form** `https://forms.gle/esDxHsvfzffYHVAZ9`: Kaggle link, GitHub link, PDF.

**Questions the team may send to the teaching assistant:** three or five metrics; is the introduction's split binding; is scikit-learn's MLP acceptable; what "preprocessing-order experiments" means. Our defaults are already what we do.

---

## PART 11: TIME

The brief's deadline was **18 October 2026, 11:59 PM**; the full run that this prompt describes was saved at 00:15 on 19 October. Ask the team about the submission status before planning (whether anything was already submitted, or whether a late or updated submission is possible); do not assume. If time is short, the order of value is: a run-all notebook on Kaggle → the PDF report → the tidy list.

---

## PART 12: WHAT TO DO NOW

1. Do Part 1 and the verification.
2. Reply with: (a) a short summary of where we are; (b) anything in the files that contradicts this prompt or looks wrong; (c) the submission status question (Part 11); (d) a plan for the tidy list (Part 9), starting with the gradient-boosting question.
3. Then wait for the team's answer.
