# HANDOFF PROMPT: copy everything below this line into a new conversation

You are continuing, as if you were the same assistant, a project that I (the team leader) have been building with Claude in another conversation. You are **Claude Code inside VS Code** on a Windows machine, with access to my project folder. Do not start working until you have done Part 1 completely. Then give me the summary described in Part 9, and wait for my confirmation before you change anything.

Today's date is **13 October 2026**. The deadline is **18 October 2026, 11:59 PM**, so about **5 days** remain.

---

## PART 1: READ EVERYTHING FIRST (do not skip anything, do not skim)

Project folder: `C:\Users\harho\OneDrive\Desktop\ACL 2\VSCode`

I want you to understand **every single tiny thing**. Read the files in this order and read each one completely:

1. **`M1 Desc.pdf`**: the official Milestone 1 brief (what we are graded on). Read every line.
2. **`ACL formula 1 intro.pdf`**: the Formula 1 introduction (domain rules, glossary, leakage hints, era table, split boundaries).
   - The Read tool returned these PDFs without content in the first conversation. Use `pdftotext` (it exists at `/mingw64/bin/pdftotext` in the Git Bash shell): run it with `-layout` and again with `-raw` (the `-raw` mode keeps the table cells in a readable order).
   - Some symbols come out as "�": they are `<=` and `>=` (for example `positionOrder <= 3`, train `<= 2019`, test `>= 2022`).
3. **`F1_decisions.md`**: the **most important file**: the 10-step plan with statuses, every decision (74 rows, A to M) with a "Decided" column, the quantitative reasoning behind B1/B3/B4, and 33 edge cases.
4. **`F1_podium_prediction.ipynb`**: the main notebook (177 cells). It is **too large for the Read tool** (more than 25,000 tokens). Read it with a short Python script that loads the JSON and prints every cell (type, id, full source, and the markdown text). Read **all** cells, in order, including markdown results and notes.
5. **`README.md`**, **`F1_project_explained.md`**, **`F1_data_overview.md`**, **`F1_table_reference.md`**, **`F1_EERD.md`**, **`F1_EERD.svg`**, **`F1_relationships.svg`**: background documents written earlier. Where they disagree with the notebook or `F1_decisions.md`, **the notebook and `F1_decisions.md` win** (see Part 7 for the known superseded statements).
6. **`csvs/`**: the 14 CSV files: `circuits`, `constructor_results`, `constructor_standings`, `constructors`, `driver_standings`, `drivers`, `lap_times`, `pit_stops`, `qualifying`, `races`, `results`, `seasons`, `sprint_results`, `status`. Look at the first rows and the columns of each one yourself, even though the notebook does it too.
7. **Git**: run `git log --oneline` and `git status`. The remote is `https://github.com/esralsayed/ACL-milestone1.git`, branch `main`. The last commit when this prompt was written was `9025481 up to EDA` (pushed). Since then only `F1_decisions.md` (step 6 marked Done) was edited and `HANDOFF_PROMPT.md` was added, both uncommitted.

### Verify the state before you trust my summary
After reading, check these facts yourself and tell me if anything differs:
- The notebook has **177 cells** and contains the section `# Exploring the Data (EDA)` and ends with `### Summary of the exploration`.
- `F1_decisions.md` says "Decided so far: A1, A2, A3, A4, B1, B2, B3, B4, D1, E3, E4 (partly), F6" and steps 1 to 6 are "Done".
- `.venv` has pandas 3.0.6, numpy, matplotlib, seaborn, scikit-learn, shap, lime, ipykernel. **No PyTorch / TensorFlow / Keras** is installed yet.

---

## PART 2: WHO I AM AND HOW I WANT YOU TO WORK

### Professional standards (these override politeness; read them twice)
Work as a **professional data analyst / data engineer**, not as an assistant that agrees with me.
- **Do not just agree with me.** If something I say or ask for does not make sense, is weaker than an alternative, or is wrong, **say so clearly and show the evidence**, before doing it. Disagreeing is part of the job. If I insist after you have given the evidence, then do it my way and note the limitation.
- **Always aim for the best solution available**, not the first one that works. For every non-trivial choice, compare the realistic alternatives with numbers, recommend the strongest one, and say what its cost or risk is. If my suggestion is not the best, tell me which is and why.
- Check the **soundness** of every step: leakage (is this known before the race?), grain (one row per driver per race?), missingness, selection bias, era effects, sample size, and whether a statement is a proof or only a proxy. Say which one it is.
- **Every number, count, name, year or fact you give me must come from the CSV files** (through code you actually ran, or an output already in the notebook). **Never invent or recall a number from memory.** Before you state a figure, compute it.
- **Do not use outside knowledge about Formula 1 as evidence.** If you use general domain knowledge (for example "why a swap happens"), say clearly that it is *not from the data* and keep it out of the notebook's evidence. The introduction PDF and the brief are allowed sources; mark them as such.
- Do not refer to a file, column, cell, variable or decision unless you have **opened and verified it exists** in this project. If you are unsure, check first.
- If you discover that something you (or the earlier conversation) said earlier is wrong, **correct it explicitly** and fix every place it appears (notebook, decisions file).
- Prefer the **simplest correct** approach; do not add complexity I did not ask for, but do tell me if the simple approach hides a risk.

### Working style

- I am the **team leader** of a university team. In the evaluation **every team member can be asked about any step**, and "an AI tool suggested it" is not an accepted justification. So **every claim must be backed by code output or a number**, and I must be able to explain it simply.
- I prefer **simple English**, brief comments, and short explanations. When I say "explain like I'm 5", use toy-car style analogies with real numbers. Do not complicate things I did not ask for.
- **Quantitative reasoning**: when I ask "why this decision / why not the others", give numbers for every option, not opinions.
- **The notebook must assume no prior domain knowledge.** Everything we claim about the data is *discovered by code first* (for example: we found that `\N` means "no value" by counting where short values appear, we did not assume it).
- **Decisions are mine to make.** Lay out options with numbers, recommend one, then wait. Record each decision in `F1_decisions.md` (with the quantitative reasoning) **only after I confirm**. Never present an undecided item as decided.
- The decision list and edge cases live in **`F1_decisions.md`, not in the notebook** (I asked for them to be removed from the notebook).
- Each table gets **its own markdown cell and its own code cell**, in the order of the table hierarchy (level 0 lookups, then `races`, then the level-2 tables).
- When I say "analyze", I mostly mean **written reasoning**; add code only when a claim needs evidence or when I ask for it.
- If I point out that something you said is wrong, **check it in the data, then say plainly what was wrong** and fix the notebook text. (This happened several times; examples in Part 7.)
- Do **not** commit or push to GitHub unless I ask. I do the commits myself.

---

## PART 3: TECHNICAL GOTCHAS (learned the hard way)

1. **VS Code overwrites your edits.** When the notebook is open with unsaved changes, VS Code saves its own copy over the file you wrote, and your new cells vanish. I often say "add again because I didn't save". Before adding cells, check what is on disk (cell count and last cells), and after writing, tell me to **close the notebook without saving or run `File: Revert File`, check the cell count, then press Ctrl+S**.
2. **`NotebookEdit` fails on this notebook** ("File has been modified since read") because the notebook is too large to Read. Edit the notebook with a Python script that loads the `.ipynb` JSON, inserts or changes cells (fresh 8-character ids), and writes it back with `json.dump(nb, f, indent=1, ensure_ascii=False)`. Always **test the new code by executing the earlier notebook cells in a namespace first**, then the new cells, and print the output before you write any interpretation.
3. **Run Python with the project venv**: `.venv/Scripts/python.exe` (system Python only has pandas and numpy). Do not use `python -I` for scripts that import sibling files.
4. **Pandas 3 behaviour**: `groupby(...).apply(...)` needs `include_groups=False`; text columns have dtype `str`; counts that mix `NaN` print as `85.0` (cast or format them).
5. **Backslash trap**: the placeholder is the two characters `\N`. In Python source use `"\\N"` (or `chr(92) + "N"`). `"\N"` is a syntax error.
6. **Windows console encoding is cp1252**: set `PYTHONIOENCODING=utf-8` and avoid printing `→` or accented names (`González` prints as `Gonz�lez`; the data is fine).
7. **Bash quoting**: long scripts with nested quotes inside heredocs break. Write scripts to files with the Write tool and run them.
8. **Scratchpad** for temporary scripts and PNGs: `C:\Users\harho\AppData\Local\Temp\claude\c--Users-harho-OneDrive-Desktop-ACL-2-VSCode\914ab3c4-a08c-4619-a1cc-d79c21bb4db7\scratchpad` (a new conversation may get a different scratchpad directory; use the one in your own system prompt).
9. To check a plot, render it to PNG (`matplotlib.use("Agg")`, patch `plt.show` to `savefig`) and **look at the image** before describing it.
10. Chrome exists at `C:\Program Files\Google\Chrome\Application\chrome.exe`; headless `--screenshot` renders SVG files for checking.

---

## PART 4: THE PROJECT IN ONE PARAGRAPH

**Milestone 1: Formula 1 podium prediction.** Data: Kaggle/Ergast Formula 1 World Championship, 1950-2024, **14 linked CSV tables** in `csvs/`. **Unit of analysis**: one driver in one race (one row per `raceId` + `driverId`). **Target**: podium = `positionOrder <= 3`. **Cutoff**: after qualifying, before the race starts, so only information known at that moment may be a feature; results, points, status, laps, pit stops and the current race's standings are **leakage** (anything from *earlier* races is allowed). Deliverables: one run-all Jupyter notebook (audit, cleaning, three data-engineering questions, features, models, experiments, XAI, inference function), the unique driver-race modeling table, a model comparison table, ablation and preprocessing-order experiments, global and local explanations, an inference function (complete and partially-missing record), and an analytical **PDF report**. Submission: a **public Kaggle notebook link + a GitHub repo link + the PDF report**, through the form `https://forms.gle/esDxHsvfzffYHVAZ9`.

### What the brief requires (checklist, from `M1 Desc.pdf`)
- EDA **before and after** cleaning, with proper visualizations.
- Clean `\N` sentinels; semantic typing (dates to dates, lap-time strings to numeric seconds).
- **Exactly one row per (`raceId`, `driverId`)**; choose a rule for duplicates and justify it.
- Check primary keys unique and non-null, foreign keys reconcile; raw CSVs stay immutable.
- **Three data-engineering questions** (multi-hop joins, a visualization, a short note on grain, missingness and the pre-race cutoff):
  1. Which circuits convert a **front-row start** into a podium most often, and does the ranking change after the **2014 hybrid era**? Distinguish qualifying position from grid.
  2. Do drivers podium more often at a **circuit in their home country**, after controlling for starting position? (needs nationality-to-country mapping)
  3. Which constructors have the highest **mechanical-retirement rate** in 2014-2021 vs 2022-2024? (mechanical = a component failed; excludes crashes, driver errors, regulation decisions)
- Feature selection justified with evidence; a leakage-safe **form** feature built from past races only; a train/validation/test split that is justified (the intro gives: **train <= 2019, validation 2020-2021, test >= 2022**).
- Models on the same rows and features: **at least two statistical ML models** plus a **shallow neural network (1-2 hidden layers)**, a baseline, and at least **three distinct modeling attempts**. Metrics: **ROC-AUC, PR-AUC, F1** (the brief later says "all five metrics" but lists only three; add precision and recall, or ask). Report train/validation **and** unseen test. **Thresholds and hyperparameters on train/validation only, never test.**
- **Feature-group ablation** and **at least two preprocessing-order experiments**.
- **XAI**: permutation importance and SHAP (global), plus a local explanation (LIME and/or SHAP waterfall); state explicitly that **importance is not causation**.
- Report: written answers to Q1-Q3 with figures, selected features and why each is valid pre-race, known limitations (qualifying-coverage drift, era sensitivity).
- Notebook sectioned, run-all ready, no hidden manual steps.

---

## PART 5: WHERE WE ARE: WHAT HAS BEEN DONE (steps 1 to 6 of 10)

### The notebook `F1_podium_prediction.ipynb` (177 cells), outline
1. Title, imports, load every CSV **as plain text** into the dict `text` (no conversions; `DATA_DIR = Path("csvs")`).
2. First look: first 2 rows of every table. "The tables and how they connect" (hierarchy and one-line description per table).
3. **Missing values, table by table** (helper `missing_report`, placeholders list, blank cells counted): one header, one check, one result per table; notes about which columns we keep.
4. **Formats and data types, table by table** (helpers `written_as`, `format_report`; `num` stands for any number): one header, one check, one result per table.
5. **Keys and links**: `PRIMARY_KEYS`, `FOREIGN_KEYS`, checks `pk_check` and `fk_check`; diagram `F1_relationships.svg`; table of the 23 one-to-many relationships.
6. **Duplicates**: identical rows; repeated (`raceId`,`driverId`) pairs; a first **join** of `results` with `races`, `drivers`, `status` (table `info`); examples; what differs inside a pair; the **three scenarios** and how they were found; whether `resultId` order tells which row is original; the rule comparison; **applying rule B1** (result: `results_one_row`); validation that no podium place is left empty; B3 (shared places); B4 (finishing places not 1..n).
7. **Exploring the Data (EDA)**, 6 analyses with plots and notes, then a summary table (uses table `eda`, `with_q`).

Key variables (strings unless noted): `text` (all raw tables), `info` (results joined with names, ints), `repeated`, `rep`, `scenarios`, `raw_results`, `results_one_row` (26,668 rows, **strings**), `eda` (ints, `year`, `podium`, `era`), `with_q`, `per_era`, `per_season`.

### Facts about the data (all verified by code)
- **Sizes**: seasons 75; circuits 77; drivers 861; constructors 212; status 139; races 1,125 (1950-2024, 7 to 24 per season); results 26,759; qualifying 10,494 (494 races, **1994 onward**); sprint_results 360 (18 races: 3 in 2021, 3 in 2022, 6 in 2023, 6 in 2024); driver_standings 34,863; constructor_standings 13,391 (**1958+**); constructor_results 12,625 (1958+); lap_times 589,081 (**1996+**); pit_stops 11,371 (**2011+**).
- **Hierarchy**: level 0 = seasons, circuits, drivers, constructors, status; level 1 = races (points to seasons and circuits); level 2 = results, qualifying, sprint_results, driver_standings, constructor_standings, constructor_results, lap_times, pit_stops. `races` is the centre.
- **Keys**: all 14 primary keys valid (`lap_times` = `raceId`+`driverId`+`lap`; `pit_stops` = `raceId`+`driverId`+`stop`; **`sprint_results` key is `resultId`**, not `sprintResultId`). All **23 foreign keys** valid (0 broken, 0 empty). Joins keep all rows.
- **Missing values**: `\N` is the only placeholder (30 columns in 6 tables). Blank cells exist only in `qualifying.q2` (22) and `q3` (46). 8 tables have no missing values. Mostly-empty columns: session dates/times in `races` (92-98.7%), fastest-lap columns (~69%) and `time`/`milliseconds` (71%) in `results`, `drivers.number` (93%) and `code` (88%), `constructor_results.status` (99.9%).
- **Mixed-format columns** (6): `results.time`, `sprint_results.time`, `pit_stops.duration`, and `positionText` in results, sprint_results, driver_standings (`D` in 1 row), constructor_standings (`E` in 17 rows). Everything else is a clean number, date, time or text. `q1`-`q3` are all `m:ss.mmm`.
- **Identical rows**: none in any table. **Only `results` has repeated (`raceId`,`driverId`) pairs.**
- **Duplicates in `results`**: **85 pairs** (79 with 2 rows, 6 with 3 rows), **176 rows**, 91 extra rows; all in 1950-1964 plus one in 1978. In all 85 pairs the finishing place and the car number differ between the rows (two different cars). Cause: in early F1 a driver could take over another car in the same race.
- **Three scenarios** (found from three yes/no facts per pair: did any row run; does the first row match another driver; does a later row match another driver): **A = 78 pairs (92%)**: a later row is another driver's car result (the driver took over a car); **B = 4 pairs**: a row ran but no later row matches (Ascari 1951 French GP, González 1954 Belgian GP, Moss 1961 British GP, da Silva Ramos 1956 French GP); **C = 3 pairs**: no row ever ran (Ertl 1978 Italian GP, Greene 1962 British GP, Flockhart 1958 Monaco GP). "Matches another driver" = a *different* driver in the same race has the same grid and the same finishing place (a proxy; the car number agrees in 175 of 176 rows).
- **Order evidence**: the 84 later rows that match another driver always match a row stored *before* them (84 of 84); of 29 first rows that match, only 4 match a row stored before and 25 match only rows stored *after* (the other driver's row was appended later). `resultId` shows storage order, not whose car it was.
- **After rule B1**: 26,668 rows, 0 repeated pairs, podium rows 3,397 to 3,379. The 18 removed podium rows all leave the place held by another driver; no race lacks place 1, 2 or 3. Races with exactly 3 podium rows: 1,107 to 1,121; 4 races keep 4.
- **Shared places after B1**: 38 finishing places shared by 2+ different drivers (37 with 2 drivers, 1 with 3), all 1950-1961; **4 on the podium** (8 rows: 1951 French GP, 1951 Indy 500, 1955 Argentine GP, 1955 Indy 500), identical in every column except `resultId` and `driverId`.
- **Finishing places 1..n**: raw: 46 races with repeated places and no gaps; after B1: 28 races not exactly 1..n (21 only repeated, 4 only missing, 3 both). Renumbering would change 371 rows and flip 4 podium labels.

### EDA findings (step 6, on `results_one_row`)
1. **12.7% podium** (3,379 of 26,668); "always no" would be 87.3% accurate, so accuracy is misleading. The rate per era (9.5% in 1989-94 to 15.0% in 2022-24) equals **3 / cars per race** (correlation per season 0.995).
2. **Podium rate by grid**: grid 1 is 50.3% (1950-1980), 56.7% (1981-2000), 76.9% (2001-2013), 81.2% (2014-2021), 79.4% (2022-2024); correlation grid vs podium -0.39 to -0.52. Strong in every era, steeper in recent eras. (Single points are noisy: 68 races in 2022-24.)
3. **Qualifying coverage**: none before 1994; 88% in 1994; 100% in 1995; 6-59% in 1996-2002; at least 98.9% every season from **2003** (22 seasons).
4. **`grid = 0`**: 1,635 rows (6.1%); 1,563 never ran (0 laps), 72 ran (all 2015-2024, pit-lane starts); 0 podiums.
5. **Cars per race**: peak 38.8 rows in 1989; 1990 has 33.9 rows vs 25.9 with a grid position (about 8 non-starters per race); about 20-24 from 1996.
6. **Qualifying position vs grid**: same in 98.4% of rows in 1994-2003 and 72.0% in 2004-2024 (22.0% start ahead, 6.0% behind); overall 76.7%.

---

## PART 6: DECISIONS ALREADY TAKEN (12 of 74)

| ID | Decision | Detail |
|---|---|---|
| A1 | What counts as missing | Both `\N` and blank text |
| A2 | Lap times as numbers | **Seconds** (`1:26.572` to 86.572); one rule works because `q1`-`q3` share one format |
| A3 | Mixed-format time columns | **Not converted**: they are post-race or replaced by another column (`results.time`, `sprint_results.time`, `pit_stops.duration`, every `positionText`) |
| A4 | Columns to keep | `races`: `raceId, year, round, circuitId, name, date` · `results`: `raceId, driverId, constructorId, grid, positionOrder, points, statusId` · `qualifying`: `raceId, driverId, position, q1, q2, q3`. **Drop**: session dates/times, `drivers.number`/`code`, `constructor_results.status`, race-time and fastest-lap columns. *(Note: values of `time`/fastest lap from **earlier** races are allowed and relevant; they are not used because they are missing for ~70% of rows (nothing before 2004) and not comparable between circuits. I suggested softening the wording to "not used for now; may be tested in the ablation". You have not answered; the notebook currently says "we do not use them".)* |
| B1 | Which row to keep when a driver has 2-3 rows in a race | **Keep the first row (lowest `resultId`)**, the car he started in. Rejected: best finishing place (80 of 85 kept rows would be another car's result; grid off by 4.5 places on average), most laps (same), last row (78 of 85, grid gap 6.1), drop the driver (176 rows instead of 91), "non-zero grid" (decides 0 of 85 pairs: 82 have non-zero grid in every row, 3 have 0 in every row), **best grid** (picks a different row in 27 pairs and 24 of them look copied; grid improves 8.5 places), **refined rule** (prefer a row no other driver shares; changes only 3 pairs; **not used**). Cost: 16 podium labels (0.06%). **Applied** in the notebook, producing `results_one_row`. |
| B2 | Grid and team | Both come from the same kept row |
| B3 | Two different drivers with the same finishing place | **Keep both drivers** (nothing separates them; 4 labels difference = 0.015%; matches the official classification). Cost: 4 races have 4 podium rows, so "exactly 3 podium predictions per race" cannot be forced |
| B4 | Finishing places not 1..n | **Accept as they are, no renumbering** |
| D1 | Target | `positionOrder <= 3`; `positionOrder` is never missing (unlike `position`, 41% empty) |
| E3 | Empty `q2`/`q3` | **Not filled**; turned into one number, the driver's best qualifying time from whichever of `q1`-`q3` exists |
| E4 | Compare lap times between races | **Partly**: gap to the fastest driver in that race; seconds vs % still open |
| F6 | `D`/`E` labels in standings | Ignore `positionText`; use `position` |

---

## PART 7: KNOWN LIMITATIONS AND CORRECTIONS (be honest about these; do not re-introduce old errors)

**Limitations of decision B1** (stated in the notebook and the decisions file):
- There is no column that says "same car"; the match on car number, grid and finishing place is a **proxy**.
- In **3 of the 4 scenario-B pairs** the first row is the one that matches another driver; the data cannot show which of the two cars he started in. In **26 scenario-A pairs** the first row also matches another driver (ambiguous). In 56 pairs the first row matches nobody; in 25 it matches only rows stored after it; in 4 it matches a row stored before it.
- No ground truth exists for "his own car". The 85 pairs are almost all before 1965, so they disappear if we model only recent seasons.
- Some wording in the notebook cell "Why this rule, and why not the others" still says a matching first row "does not make it wrong"; this is an assumption supported by the order evidence for 25 of 29 rows, not proven.

**Statements that were wrong earlier and were corrected (never repeat them):**
- Race start `time` exists from **2005**, not 2006.
- The `sprint_results` key is `resultId`, not `sprintResultId`.
- "59 stand-alone shared cars" was wrong; the right count is **25 stand-alone shared places** (105 shared places before B1: 80 seen from a swap, 25 stand-alone; **38** after B1). Some car numbers are used by 2+ drivers only because one of them never started (31 of 140).
- "`grid = 0` means a pit-lane start" is true only from 2015 (72 rows); before that it almost always means the driver never started.
- "The first row is always the driver's own car" is **not** established (see the limitations above).
- The three scenario-C pairs are **Ertl (1978 Italian GP, Did not qualify with ATS and Did not prequalify with Ensign), Greene (1962 British GP, Withdrew with Lotus-Climax and with Gilby) and Flockhart (1958 Monaco GP, Did not qualify with Cooper and with BRM)**. In all three the driver was listed with two teams and neither entry ran; the data does not say why.
- Podium rows per race: raw had 16 races with 4, one with 5 and one with 7 podium rows; after B1, 1,121 races have 3 and 4 have 4.
- The earlier documents `F1_project_explained.md`, `F1_data_overview.md`, `F1_EERD.md`, `F1_table_reference.md` were written before some of these checks; treat them as background only.

**Other cautions:**
- The notebook was tested cell by cell in a harness (earlier cells executed in order), **not yet as a full Restart-and-Run-All in Jupyter**. Do this before submission (and check run time: `lap_times.csv` is 16.8 MB).
- `F1_relationships.svg` is embedded by a relative link; on Kaggle it must be uploaded with the notebook (or exported to PNG).
- Several markdown notes say "decided in the cleaning step"; make sure those decisions are really written there.
- Both PDFs are course material in the public repo; I may want them excluded.

---

## PART 8: WHAT REMAINS (steps 7 to 10) AND THE 62 OPEN DECISIONS

### Step 7: Decisions and cleaning (next)
Apply A1-A4 to produce clean tables (keep only the decided columns, convert types, treat `\N`/blank as missing, `q1`-`q3` to seconds, `date`/`dob` to dates). Decide and apply the row filters: **C1** (drop drivers who never started: 1,563 rows never ran, 0 podiums, known pre-race), **C2** (definition of "started": `grid > 0` vs `laps > 0`; 966 rows have a grid slot but 0 laps, 84 "Withdrew" rows still have a grid slot), **C3** (Indianapolis 500: 11 races 1950-1960, 405 rows, 104 of 107 drivers never raced elsewhere), **C4** (which seasons: candidates all 1950+, 1994+, 2003+; qualifying is complete from 2003), **C5** (same filters for Q1-Q3?), **C6** (disqualified/excluded: 155 rows), **C7** (use sprint results? only 18 races), **E1** (`grid = 0` meaning; flag the 72 pit-lane starts), **E2** (races without qualifying), **E5** (use qualifying position, grid, or both; identical before 2004), **E6** (team id mismatch: 10 rows in 2015, "Marussia" in qualifying vs "Manor Marussia" in results), **A5** (label cleanup: `'Argentinian '` trailing space, `&amp;` in `Lotus-Pratt &amp; Whitney`, `USA` vs `United States` (2 Las Vegas races), dual nationalities), **D2** (rare podiums: class weights or none), **D3** (force exactly 3 per race?). Then **EDA after cleaning**: repeat the key plots and show before/after counts (the brief requires EDA before and after).

### Step 8: Feature engineering (leakage-safe)
Features known before the race: `grid`, qualifying best-time gap, **standings before the race** (standings rows already **include** that race's points in 99.4% of rows, so use the previous round's row; round 1 needs a rule; `(year, round)` is unique so "previous race" is easy), **recent form from past races only** (sort by date, group by driver or team, `shift(1)` before any rolling window), age from `dob`, era/field size. Open decisions: **F1-F5**, **G1-G10**, **L1-L3**. Show a plot or number as evidence for each feature.

### Step 9: The three data-engineering questions (can be split among teammates)
- **Q1**: `results` + `races` + `circuits` + `qualifying`; front row by grid and by qualifying; split at 2014; open **H1-H3** (qualifying only exists from 1994; 24 circuits were used 3 times or fewer).
- **Q2**: `results` + `drivers` + `races` + `circuits` + a **nationality-to-country mapping**; control for grid; open **I1-I5** (British to UK, American to USA, Monegasque to Monaco, Dutch to Netherlands; dual and historical nationalities; countries that never hosted a race).
- **Q3**: `results` + `status` + `races` + `constructors`; a **status-to-mechanical mapping** (62 different statuses in 2014-2024; unclear ones: `Retired`, `Technical`, `Damage`, `Collision damage`, `Puncture`, `Out of fuel`); team lineage (Force India to Racing Point to Aston Martin; Toro Rosso to AlphaTauri to RB; Sauber to Alfa Romeo; Lotus F1 to Renault to Alpine; Marussia to Manor); open **J1-J5**.

### Step 10: Split, models, experiments, XAI, inference, report
Open **K1-K6** (confirm split; **main/second metric**, my leaning is PR-AUC main because podiums are rare, justified by EDA section 1; threshold chosen on validation; "five metrics"; retrain on train+validation?; treat 2020 as normal?), **L4-L10** (two preprocessing orders; baseline; second statistical model; **neural network library: PyTorch/Keras not installed**; tuning; ablation feature groups; random seed), **M1-M4** (which model to explain; which local example; prediction function input format; which incomplete record). Deliver: model comparison table (validation and test), ablation, preprocessing-order experiments, permutation importance + SHAP + LIME/SHAP waterfall (not causal), inference function on a complete and a partially-missing record, and the **PDF report**.

### Full list of the 62 decisions still open
A5 · C1, C2, C3, C4, C5, C6, C7 · D2, D3 · E1, E2, E5, E6 · F1, F2, F3, F4, F5 · G1-G10 · H1-H3 · I1-I5 · J1-J5 · K1-K6 · L1-L10 · M1-M4 (the options, evidence and counts for each are in `F1_decisions.md`).

### Suggested time plan (5 days: 13-18 October)
| Day | Work |
|---|---|
| 13-14 Oct | Step 7 (cleaning) and EDA after cleaning; start step 8 |
| 14-15 Oct | Step 8 (features); Q1-Q3 in parallel with teammates |
| 15-17 Oct | Step 10: split, models, experiments, XAI, inference function |
| 17-18 Oct | Report (PDF), full Restart-and-Run-All, Kaggle upload, push to GitHub, submit |

---

## PART 9: WHAT I WANT FROM YOU NOW

1. Do **Part 1** completely (read all files, print all notebook cells).
2. Run the checks in "Verify the state".
3. Reply with **(a)** a short summary in your own words of where we are, **(b)** the decisions taken and the ones still open (grouped), **(c)** what is missing, **(d)** anything in the files that contradicts this prompt or looks wrong, and **(e)** as a professional reviewer, **any decision already taken that you think is weak, risky or not the best option, with the evidence from the data** (for example the first-row rule B1, keeping both drivers B3, or the choice of columns A4). Challenge them honestly; do not assume the earlier conversation was right.
4. Then **ask me which step to start with** (I expect step 7: cleaning, beginning with C1 and E1, which now have evidence) and wait for my answer. Do not edit the notebook, the decisions file, or git until I confirm.
