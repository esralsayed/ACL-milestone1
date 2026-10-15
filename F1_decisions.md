# F1 Podium Project: Decisions and Edge Cases

Working list of every decision the project needs and every edge case found in the data. Kept outside the notebook; the notebook discovers these facts with code.

## Plan: the steps, in order

Notebook: `F1_podium_prediction.ipynb`. Deadline: **18 October 2026, 11:59 PM**. Update the **Status** column as we go.

| #   | Step                                                                  | What happens                                                                                                                                                                                                                        | Decisions settled here                                | Status                                                                                            |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 1   | Load the data and first look                                          | Load every CSV as plain text; look at the first rows of each table; describe the tables and how they connect                                                                                                                        | –                                                     | Done                                                                                              |
| 2   | Missing values, table by table                                        | Count blank cells and placeholders per column; for each table say whether the gaps matter and which columns we keep                                                                                                                 | A1, A4, D1, E3, E4 (partly)                           | Done                                                                                              |
| 3   | Formats and data types                                                | Find columns written in more than one format (e.g. race times, pit-stop durations) and text that should be numbers or dates                                                                                                         | A2, A3, F6                                            | Done                                                                                              |
| 4   | Keys and links                                                        | Check primary keys (unique, never empty) and foreign keys (every link points to a real row)                                                                                                                                         | –                                                     | Done                                                                                              |
| 5   | Duplicates                                                            | Fully identical rows, repeated IDs, and the same driver twice in one race (shared cars); choose and explain a rule                                                                                                                  | B1-B4 (all decided)                                   | Done (checks, scenarios, B1 rule, B3 and B4 are in the notebook; `results_one_row` is the result) |
| 6   | Exploring the data (EDA)                                              | Podium rate, grid vs. podium, qualifying coverage per season, `grid = 0`, number of cars per race, with plots                                                                                                                       | – (gives the evidence for step 7)                     | Done (6 analyses and a summary table in the notebook)                                             |
| 7   | Decisions and cleaning                                                | Drop unused columns, fix duplicates, choose rows and seasons, fix labels; show before/after counts and repeat key plots                                                                                                             | C, D2, D3, E1, E2, E4-E6, F1-F5, A5 (and apply A1-A4) | To do                                                                                             |
| 8   | Feature engineering                                                   | Build features using only information known before the race: grid, qualifying, standings before the race, recent form from **past races** (sort by date, group by driver / team, shift by one race); show evidence for each feature | G, L1-L3                                              | To do                                                                                             |
| 9   | The three data-engineering questions                                  | Q1 front row → podium by circuit, Q2 home advantage, Q3 mechanical failures by team; each with joins, a plot and an answer                                                                                                          | H, I, J                                               | To do (after step 7)                                                                              |
| 10  | Split, models, experiments, explanations, prediction function, report | Season split, baseline + second model + small neural network, ablation and preprocessing-order experiments, SHAP / LIME, prediction function, PDF report                                                                            | K, L4-L10, M                                          | To do                                                                                             |

**Rule for past-race features (step 8):** for the race being predicted, only use what is known before it starts: anything from **earlier** races (positions, points, status, standings after the previous race) plus this race's grid and qualifying. Never use this race's own result, points, time or status (that is leakage).

## Decisions to Take

Every choice the project needs, from the biggest to the smallest. When a decision is made, the **Decided** column gives the choice and where it is written in the notebook (section → table). Everything else is still **open**.

**Deferred to step 10 (decided by experiment, not by argument):** C4, the choice between `q1` only and the best of `q1`-`q3` (E3), and the unit and cap of the qualifying gap (E4). See "Experiments to run in step 10" below (the filter on `has_qualifying` and the fill of E2 are X1, X2 and X5).

**Decided so far:** A1, A2, A3, A4, A5, B1, B2, B3, B4, C1, C2, C3, C6, C7, D1, E1, E2 (the cleaning rule; the fill is experiment X5), E3, E4 (partly), E5, E6, F1, F2 (by F1), F3, F4, F5, F6, G1, G2, G3, G4, G5, I1, I2, I3 (by A5), I4, I5.

### A. Loading and data types

| #   | Decision                           | Options                            | Why it matters                                                                                           | Decided                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| --- | ---------------------------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A1  | What counts as an empty value      | Only `\N` · also blank text        | `q2` / `q3` have 22 / 46 blank cells besides `\N`                                                        | **Both `\N` and blank text are missing.** (Missing values → `qualifying`)                                                                                                                                                                                                                                                                                                                                                                                          |
| A2  | How to turn lap times into numbers | Seconds · milliseconds             | `q1`-`q3` are text like `1:27.452`                                                                       | **Seconds**, e.g. `1:26.572` → 86.572. All `q1`-`q3` use one format (min:sec), so one rule works. (Formats → intro, `qualifying`)                                                                                                                                                                                                                                                                                                                                  |
| A3  | What to do with mixed-format times | Convert · drop the column          | `pit_stops.duration` is `26.898` or `16:44.718`; `results.time` is the winner's time or a gap (`+5.478`) | **Not converted.** All mixed columns (`results.time`, `sprint_results.time`, `pit_stops.duration`, every `positionText`) are post-race or replaced by another column, so they are not used. (Formats → `results`, `sprint_results`, standings, `pit_stops`)                                                                                                                                                                                                        |
| A4  | Which columns to drop as useless   | e.g. `url`, practice dates, `code` | Practice and qualifying dates are empty before 2021                                                      | **Keep only:** `races`: `raceId`, `year`, `round`, `circuitId`, `name`, `date` · `results`: `raceId`, `driverId`, `constructorId`, `grid`, `positionOrder`, `points`, `statusId` · `qualifying`: `raceId`, `driverId`, `position`, `q1`-`q3`. **Drop** e.g. session dates/times, `drivers.number` / `code`, `constructor_results.status`, race-time and fastest-lap columns. (Missing values → `drivers`, `races`, `results`, `qualifying`, `constructor_results`) |
| A5  | How to clean text labels           | Strip spaces · fix `&amp;`         | `'Argentinian '` (trailing space), `Lotus-Pratt &amp; Whitney`                                           | **Explicit dictionary of 3 corrections, applied to copies (raw tables unchanged):** `'Argentinian '` → `Argentine`; `United States` → `USA`; `&amp;` → `&`. Spaces are removed around every text value. Accents and names are not changed. Reasoning below; code in the notebook ("Cleaning the text labels (decision A5)").                                                                                                                                       |

### B. One row per driver per race (duplicates)

| #   | Decision                                                 | Options                                                                                          | Why it matters                                                                                                | Decided                                                                                                                                                                                                                                                                                   |
| --- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| B1  | Which row to keep when a driver has 2-3 rows in one race | Best finishing position · the car he started in (first `resultId`) · most laps · drop the driver | 85 cases (176 rows). The brief's "non-zero grid" rule fails: in 82 of 85 cases both rows have a grid position | **Keep the row of the car the driver started in: the row with the lowest `resultId` of each pair.** Reasoning below. **Applied** in the notebook (Duplicates → "Applying the rule"): 26,759 → 26,668 rows, 91 removed, new table `results_one_row`.                                       |
| B2  | Which grid and team to keep for that driver              | Take them from the kept row · from the car he started in                                         | If the kept row is the car he took over, its grid is that car's, not his own                                  | **Grid and team come from the same kept row**, so they describe the car he started in. (Same row as B1; nothing is mixed from the other row.)                                                                                                                                             |
| B3  | What to do when two drivers share one car's result       | Both get the podium · only one · drop                                                            | 18 races have 4, 5 or 7 podium rows because of shared cars                                                    | **Keep both drivers.** Every driver who shares a finishing place keeps his own row and the same label. After B1 this affects 38 shared places (77 rows), of which only 4 are on the podium (8 rows, in 1951 and 1955). Reasoning below.                                                   |
| B4  | Accept races where `positionOrder` is not 1, 2, 3, ...   | Accept · renumber                                                                                | 46 early races (all before 1965)                                                                              | **Accept the finishing places as they are, no renumbering.** Renumbering would change 371 rows in 28 races and flip 4 podium labels (the shared podium places), contradicting B3. Only places 1-3 are used by the target, and no race is missing place 1, 2 or 3. (Duplicates → B4 cells) |

#### Why B1 and B2: keep the car the driver started in (quantitative reasoning)

Numbers are from the repeated pairs in `results`: 85 driver-race pairs (79 with 2 rows, 6 with 3 rows), 176 rows, 91 of them "later rows" (a pair's rows other than the first). They fall in 1950-1964, plus one pair in 1978. "First row" = lowest `resultId` of the pair.

1. **The rows of a pair are different cars.** In all 85 pairs the car numbers differ between the rows (0 pairs share a number). Inside one race a car number identifies a car: 26,452 of 26,592 (race, number) combinations belong to a single driver.
2. **The later row is usually another driver's car result.** 84 of the 91 later rows (92%) have the same grid and finishing place as another driver's row in the same race. Only 29 of the 85 first rows (34%) do, and that figure is an upper bound: it also counts a first row whose car was later taken over by someone else (the first row is still the driver's own car).
3. **Effect of each rule on the 85 kept rows** (rows that carry another car's grid and place):

| Rule                              | Kept rows carrying another car's grid and place | Podium rows among the 85 |
| --------------------------------- | ----------------------------------------------- | ------------------------ |
| **First row (car he started in)** | **29 (34%)**                                    | 6                        |
| Best finishing place              | 80 (94%)                                        | 22                       |
| Most laps                         | 80 (94%)                                        | 22                       |
| Last row                          | 78 (92%)                                        | 17                       |

4. **The grid error of the alternative is large.** `grid` is our strongest feature. In the 64 pairs where "best finishing place" picks a different row than "first row", the grid differs by **6.0 places on average** (median 5.5, maximum 18).
5. **The cost is small.** Keeping the first row gives 6 podium rows instead of 22 among these pairs: **16 podium labels**, i.e. 0.06% of the 26,759 rows (3,379 podium rows overall instead of 3,395). In 21 of the 85 pairs one row is a podium and the other is not, so this is where the labels change.
6. **The brief allows it.** It names "the car the driver started in" as an acceptable rule.

**What we give up:** a driver who retired and then finished on the podium in another car loses that podium label. This is a known limitation and is stated in the report.

**Limits of the evidence:** there is no ground truth for "his own car"; the rule rests on points 1-2. The data does not say why a swap happened (59 first rows stopped during the race, 22 have a normal finishing place, 4 did not qualify, withdrew or were disqualified), and the rule does not depend on it. Almost all pairs are before 1965, so if only recent seasons are modeled they disappear anyway.

**B1 confirmed after the follow-up checks (plain first row).** The refined rule (prefer a row that no other driver shares, otherwise the first row) would change only 3 of 85 pairs (the scenario-B pairs Ascari 1951, González 1954, Moss 1961) and is not used; best grid was also rejected (it picks a different row in 27 pairs and, in 24 of them, keeps a row that matches a row stored before it, with the grid improving by 8.5 places on average). Known limitation: the file has no column that says "this is the same car", so a match on car number, grid and finishing place is only a proxy (the two signals agree on 175 of 176 rows); `resultId` order shows when a row was stored, not whose car it was. Distribution of the 85 pairs: scenario A 78 (92%), B 4 (5%), C 3 (3%). In 56 pairs the first row matches no other driver, in 25 it matches only rows stored after it, in 4 it matches a row stored before it.

#### Why B3: keep both drivers who share a finishing place

Counts are after applying B1 (26,668 rows).

1. **The data cannot tell the sharers apart.** In the 4 shared podium places (1951 French GP, 1951 Indy 500, 1955 Argentine GP, 1955 Indy 500) the two drivers have the same team, car number, grid, finishing place, points and laps. Any rule that picks one of them (`resultId`, `driverId`, alphabetical) is arbitrary.
2. **The size is tiny.** 38 shared places remain (37 with 2 drivers, 1 with 3), all in 1950-1961; only 4 places (8 rows) are on the podium. Keeping both gives 3,379 podium rows; keeping one per place gives 3,375 (4 labels fewer, 0.015% of 26,668 rows).
3. **It matches the official classification**, where both drivers are credited with the result (points are split, e.g. 1.33 each).
4. **Alternatives cost more.** Neither counts: 3,371 podium rows (8 real podium finishes lost). Drop the rows: 8 rows removed (77 if all shared places are dropped).
5. **It works for any number of sharers.** Up to 5 drivers share one result in the raw data (1954 Indianapolis 500, place 11); after B1 none of the groups of 3 or more is on the podium.

**Cost of keeping both:** 4 races have 4 podium rows instead of 3, so "exactly 3 podium predictions per race" (D3) cannot be forced in those races. All shared podium places are in 1951 and 1955, so none remains if only recent seasons are modeled.

**B4 (decided):** 46 raw races have repeated places and no gaps; after B1, 28 races are not exactly 1 to n (21 only repeated, 4 only missing, 3 both). Accepted as they are. Note: some car numbers are used by 2+ drivers in a race only because one of them never started (31 of 140 such numbers); these are not shared results.

### C. Which rows to keep

| #   | Decision                                             | Options                                                                 | Why it matters                                                                                                                                                      | Decided                                                                                                                                                                                                                                                                                                          |
| --- | ---------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| C1  | Keep drivers who never started?                      | A keep all · **B drop `grid = 0`** · C drop `grid = 0` before 2015 only | 1,635 rows have `grid = 0` (6.1%), none is a podium. The grid slot is known before the race                                                                         | **B: remove every row with `grid = 0`** (26,668 → 25,033 rows; all 3,379 podium rows stay). The filter uses only `grid`, never `laps` or `status` of the race. Reasoning below.                                                                                                                                  |
| C2  | How to define "started the race"                     | `grid > 0` · `laps > 0` · either · by status                            | 966 rows have a grid slot but 0 laps (lap-1 crashes); 84 "Withdrew" rows still have a grid slot                                                                     | **A: "started" means a grid slot (`grid > 0`) and nothing else.** Rows with a grid slot and 0 laps (966) stay, and so do rows whose status says Withdrew / Did not qualify / Excluded but have a grid slot (98). `laps` and `status` of the race are post-race and are not used to select rows. Reasoning below. |
| C3  | Keep the Indianapolis 500?                           | Keep · drop                                                             | 11 races (1950-1960); 381 rows after B1 (405 raw); 103 of its 107 drivers never raced elsewhere in F1 (corrected from 104: only Ascari, Ward, Ruby and Ruttman did) | **Drop the Indianapolis 500** (381 rows, 11 races, 35 podium rows: 3,379 → 3,344). Reasoning below; evidence code in the notebook ("Cleaning: which rows stay" → C3).                                                                                                                                            |
| C4  | Which seasons to model                               | All (1950+) · 1994+ · 2003+ · 2006+                                     | Qualifying data: none before 1994, patchy until 2002, complete from 2003                                                                                            | **Deferred to step 10 (experiment).** The cleaned table keeps all seasons (1950-2024); the modeling window is chosen by comparing the windows listed in "Experiments to run in step 10". Evidence so far is exploratory only.                                                                                    |
| C5  | Use the same row filters for Q1-Q3 as for the model? | Same · decide per question                                              | Q1 can use all years for grid; Q3 only needs 2014-2024                                                                                                              | **Follows from C4:** Q1-Q3 use the full cleaned table (all seasons); only the models use a training window.                                                                                                                                                                                                      |
| C6  | Keep disqualified / excluded drivers?                | Keep · drop                                                             | 155 rows in the raw table by status (147 Disqualified, 8 Excluded); 146 rows flagged in the table after B1, C1 and C3; they raced but lost their result             | **Keep them.** Their label is the official classification (not a podium). Nothing is removed (24,652 rows, 3,344 podium rows). Reasoning below; evidence code in the notebook ("Cleaning: which rows stay" → C6).                                                                                                |
| C7  | Use sprint results as a feature?                     | Use (sprint finish, sprint points) · don't use                          | Pre-race information (1 day before the race in 18 of 18), but only 18 races (341 table rows, 1.4%) have a sprint and none is in the years up to 2019                | **Do not use.** The 341 main-race rows of sprint weekends stay (54 podium rows); only `sprint_results` is left out. Reasoning below; evidence code in the notebook ("Cleaning: which rows stay" → C7).                                                                                                           |

#### Why C1 = B and E1: remove every row with `grid = 0` (quantitative reasoning)

Counts are from `results_one_row` (26,668 rows, after B1).

**What `grid = 0` contains**

| Group                  | Rows      | Podiums | Notes                                                                                                                                       |
| ---------------------- | --------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Never ran (0 laps)     | 1,563     | 0       | 1,505 of them (96%) have status Did not qualify (1,012), Did not prequalify (330) or Withdrew (163); seasons 1952-2023                      |
| Ran, from the pit lane | 72        | 0       | All in 2015-2024 (1 in 2015, up to 16 in 2023); finishing places 5 to 22 (median 15); qualifying position known for 71 (5 to 22, median 18) |
| **Total**              | **1,635** | **0**   | 6.1% of the rows                                                                                                                            |

**Reasons for removing them**

1. **The 72 pit-lane rows are too few to teach the model anything and could add noise (team's reason).** They are 0.27% of the rows. The grid is the strongest feature (EDA 2: podium rate falls steeply with the grid, correlation -0.39 to -0.52), and a `0` read as a number sits "ahead of pole position", against that relation.
2. **A separate flag column is not worth it (team's reason).** A pit-lane flag would be 1 on 72 rows and 0 podiums. The back of the grid in 2015+ (grid 15th or worse) has 12 podiums in 1,225 rows (0.98%), so about 0.7 podiums would be expected in 72 rows. Seeing 0 is what chance gives, so there is no evidence that the flag carries a signal different from "starts at the back".
3. **The other 1,563 rows are not participants.** None can finish on the podium and the grid slot says so before the race.
4. **Keeping them flatters the scores.** AUC of the grid alone: 0.890 with them and 0.881 without (train); 0.935 and 0.923 in 1990-94; 0.914 and 0.911 in the test years. The model would be credited for "predicting" drivers who were not in the race, and the podium rate is diluted (12.7% against 13.5%).
5. **It is a pre-race rule.** The grid is known before the race. `laps` and `status` of the same race are not, so we cannot drop rows with them (see the 966 rows below).
6. **In 2015+ the two meanings cannot be separated before the race.** Of the 79 modern `grid = 0` rows, 72 ran and 7 did not; both look the same (`grid = 0`), so a rule "keep modern `grid = 0`" would keep 7 non-participants.
7. **One rule, easy to defend.** Option C needs a year boundary (2015) that we would have to justify, for 72 rows with no podium.

**Options not chosen**

| Option                             | Rows   | Why not                                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------------------ |
| A keep all                         | 26,668 | Reasons 3 and 4: 6.1% of rows are non-participants and the scores are flattered                        |
| C drop `grid = 0` before 2015 only | 25,112 | Reasons 2 and 6: keeps 79 rows (7 non-participants) that carry no usable signal, and needs a year rule |

**Costs and limitations (to state in the report)**

- The model never sees a pit-lane start (72 rows, 0.27% of the data, 0 podiums).
- The 966 rows with a grid slot and 0 laps (lap-1 crashes) **stay**: they are only known after the race starts. They carry 0 podiums but are legitimate prediction rows.
- If someone passes `grid = 0` to the prediction function, it is replaced by the last slot of that race (an assumption, not learned from data).
- The filter removes no podium row: 3,379 before and after.

#### Why C2 = A: keep every row that has a grid slot, also with 0 laps

Counts are after C1 (25,033 rows with `grid > 0`).

| Group (all have a grid slot)                 | Rows                                                  | Podiums | Top statuses                                                                 |
| -------------------------------------------- | ----------------------------------------------------- | ------- | ---------------------------------------------------------------------------- |
| 0 laps                                       | 966 (3.9%)                                            | 0       | Collision 353, Accident 233, Withdrew 61, Engine 47, Spun off 38, Gearbox 34 |
| Status Withdrew / Did not qualify / Excluded | 98 (73 of them also in the 0-lap group; 25 have laps) | 0       | Withdrew 84, Did not qualify 12, Excluded 2                                  |

**Reasons**

1. **It is the pre-race view.** At prediction time a driver with a grid slot is on the grid, and nobody knows who will be out on lap 1. A table that drops the 0-lap rows would be built with the outcome of the race itself.
2. **Same principle as C1.** C1 removed rows by `grid`, which is known before the race; C2 does not add a filter on `laps` or `status`, which are not.
3. **The 0-lap rows are not random, and the grid already carries part of it.** The share of rows with 0 laps rises with the grid slot: 2.2% for grid 1-3, 2.5% for 4-6, 3.5% for 7-10, 4.5% for 11-15, 4.8% for 16 and worse; mean grid 13.6 against 11.8 for the others. A model can use this because it only needs the grid.
4. **The effect on the scores is small, so the choice is made on principle, not on performance.** Score of the grid alone (ROC-AUC / PR-AUC), keeping against dropping the 966 rows: train 0.881 / 0.493 against 0.881 / 0.503; validation 0.907 / 0.639 against 0.911 / 0.667; test 0.911 / 0.647 against 0.910 / 0.651.
5. **They are correctly labelled.** A driver who did not complete a lap did not finish on the podium, so the label is right; these are negatives, not errors.

**What it costs:** 966 rows (3.9%) that can never be a podium, which lowers the podium rate (13.5% against 14.0% without them) and the PR-AUC slightly (test: 0.647 against 0.651 for the grid alone).

**Note:** the `laps` column of the race being predicted is not a feature (post-race) and is not in the A4 keep list. Values from earlier races are allowed and are handled in step 8 (G7, G8).

#### Why C3: drop the Indianapolis 500

Counts after B1 and C1 (all 381 rows of the race have a grid slot).

| Measure                             | Indianapolis 500 | Other races, 1950-1960 |
| ----------------------------------- | ---------------- | ---------------------- |
| Rows                                | 381 (11 races)   | 1,763                  |
| Rows per race                       | 34.6             | 21.2                   |
| Podium rate (rows with a grid slot) | 9.2%             | 14.9%                  |

1. **95% of its rows have no history.** 103 of its 107 drivers never appear in any other race; they hold 362 of its 381 rows and 32 of its 35 podium rows. Past-race features (form, team form, standings) are empty for them by construction, and they cannot be compared with regular drivers. Only Ascari, Ward, Ruby and Ruttman raced elsewhere.
2. **Its structure is different:** 34.6 rows per race against 21.2, a lower podium rate, and 21 of the 85 repeated driver-race pairs (25%) are in this race.
3. **It would distort Question 2 (home advantage)**, as the introduction warns.
4. **The cost is limited to 1950-1960:** 35 podium rows (3,379 → 3,344, 381 rows). It changes nothing for any training window that starts later.
5. **The introduction names exclusion as a defensible choice** (allowed source); the data above is our own evidence for it.

**Cost:** 35 podium rows, all in 1950-1960. Q2 loses the American drivers' Indianapolis races.

#### Why C6: keep the disqualified and excluded rows

Counts are for the table after B1, C1 and C3 (24,652 rows).

| Measure                                                                | Value                                                                                                              |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Rows flagged (status `Disqualified`/`Excluded`, or `positionText` D/E) | **146** (0.59%): 142 by both markers, 4 by the letter only, 0 by status only                                       |
| Raw table, for reference                                               | status: 147 Disqualified + 8 Excluded = 155; `positionText`: 151 D + 9 E = 160                                     |
| Podium rows among the flagged                                          | **0**                                                                                                              |
| Completed at least 90% of the laps of the race                         | 76 (13 started in the top 3, 10 of them on the front row)                                                          |
| Of those 76, ranked below all unflagged full-distance finishers        | 76 of 76                                                                                                           |
| By decade                                                              | 1950s: 5, 1960s: 9, 1970s: 25, 1980s: 51, 1990s: 20, 2000s: 22, 2010s: 9, 2020s: 5 (110 before 2000, 36 from 2000) |
| Races with a flagged row                                               | 109 of 1,114 (327 of the 3,344 podium rows are in those races)                                                     |
| Podium rate keeping / dropping                                         | 13.56% / 13.65% (3,344 podium rows either way)                                                                     |

1. **A disqualification is known only after the race.** Dropping the rows would select rows with the result of the race, which is the principle used in C1 and C2.
2. **It is consistent with D1.** The target is the final classification (`positionOrder`). In the 1983 Brazilian GP, `position` and `positionOrder` differ in 13 rows and one driver gets a podium label he would not have had; those promoted drivers are podiums _because_ of the disqualification. Removing the disqualified row but keeping the promoted ones would be inconsistent.
3. **`positionOrder` already handles them.** All 76 full-distance flagged rows are ranked below every unflagged full-distance finisher, so a disqualified driver is a clean negative.
4. **Dropping would flatter the scores.** The 13 cars that started in the top 3 and ran the full distance are the hard cases a real prediction faces.
5. **The size is negligible:** 0.59% of the rows and no podium row.
6. **No definition is needed.** Status and `positionText` differ on 4 rows; keeping all rows avoids choosing between them.

**Cost / limitation (state in the report):** about 13 drivers who looked like podium finishers on the road (top-3 grid, full distance) carry the label "not a podium". This label noise is not visible in the data.

#### Why C7: do not use the sprint results as features

Counts are for the table after B1, C1 and C3 (24,652 rows).

| Measure                                                 | Value                                                                                                                                                    |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sprint races                                            | 18 (2021: 3, 2022: 3, 2023: 6, 2024: 6); `sprint_date` is 1 day before the race date in all 18                                                           |
| Table rows in sprint weekends                           | **341** (1.4%), 54 podium rows; up to 2019: **0**, 2020-2021: 56, 2022-2024: 285                                                                         |
| Rows with a sprint result in a training window          | up to 2019: 0; up to 2021: 56 (0.24%); up to 2022: 113 (0.48%)                                                                                           |
| Podium rate: sprint weekends / other races of 2021-2024 | 15.8% / 15.4%                                                                                                                                            |
| Corr. with podium (grid on the same rows: -0.45)        | sprint place -0.47, sprint points 0.53, sprint grid -0.42, team's best sprint place -0.48, team's sprint points 0.51, places gained 0.06, completed 0.01 |
| Same, after removing what the grid explains             | -0.25, 0.38, -0.20, -0.25, 0.34, 0.02, -0.02                                                                                                             |
| Grid equals sprint place                                | 2021-2022: 62 of 113 rows (the sprint result set the Sunday grid); 2023-2024: 35 of 228                                                                  |

1. **It cannot be learned.** With the training years of the introduction (up to 2019, K1 still open) the column would be constant; training up to 2022 gives only 113 rows (0.48%).
2. **It would be empty for 98.6% of the rows.** Every fill is an assumption: 0 reads "won the sprint", a large number "finished last", a mean "midfield"; only the row's own grid position is neutral, and then the column adds nothing for 98.6% of rows.
3. **The evidence is thin:** 341 rows in 18 races, and in 2021-2022 part of the signal is the grid itself.
4. **It is not rejected for leakage:** the sprint is the day before the race, so it is pre-race information. It is left out because it cannot be trained and tested honestly. State this as a limitation in the report.
5. **No special case** for 1 row in 70; every model gets the same features.

**Cost:** a possible extra signal in the sprint weekends of 2021-2024 (the sprint place keeps a correlation of -0.25 with the podium after the grid is removed). It can be tested later as an experiment on 2021 and later only.

**Not decided here:** whether sprint failures count in Question 3 (J5).

#### Why A5: three corrections by an explicit dictionary

Checked columns: `circuits.country`, `drivers.nationality`, `constructors.nationality`, `constructors.name` (the ones Question 2 and Question 3 use).

| Problem                                                     | Evidence                                                                                                                                                                                                                                                                    | Correction              |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `'Argentinian '`: a trailing space and a different spelling | 1 driver (Colapinto) against 24 who use `Argentine`; found by exact normalisation (the space) and by string similarity (`Argentine` / `Argentinian`)                                                                                                                        | `Argentine`             |
| `United States` against `USA`                               | They share no letters, so spelling cannot find it. The only circuit labelled `United States` is Las Vegas Strip (2 races, 2023-2024); the nearest circuit is 0 km away (same coordinates), labelled `USA`, and the next four are also `USA`. 11 of 12 US circuits say `USA` | `USA`                   |
| `Lotus-Pratt &amp; Whitney`                                 | An HTML code for `&`; 1 team, 3 result rows; display only                                                                                                                                                                                                                   | `Lotus-Pratt & Whitney` |

**Not changed, and why**

- Accents are real characters. Names are not simplified: `Jos` Verstappen and `José` Dolhem, `Tom` Pryce and `Tomáš` Enge would be merged by an accent-blind comparison.
- `Australian` / `Austrian` and `Australia` / `Austria` look alike but both labels have their own drivers and circuits (20 and 16 drivers, 2 circuits each): different countries.
- Dual nationalities (`American-Italian`, `Argentine-Italian`) and the link nationality → country belong to I1 and I2.

**Method:** a dictionary shown in the notebook (variant, label kept, rows touched), applied to copies (`drivers_clean`, `circuits_clean`, `constructors_clean`); labels before and after: 43 → 42 nationalities, 35 → 34 countries, 1 → 0 `&amp;`.

### D. Target

| #   | Decision                                         | Options                                     | Why it matters                                                                        | Decided                                                                                                      |
| --- | ------------------------------------------------ | ------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| D1  | Confirm the target                               | `positionOrder <= 3`                        | `positionOrder` already includes post-race disqualifications (e.g. 1983 Brazilian GP) | **`positionOrder` 1, 2 or 3 = podium.** It is never missing, unlike `position`. (Missing values → `results`) |
| D2  | How to handle podiums being rare                 | Class weights · resampling · nothing        | About 13% podiums overall (9.5% in 1989-94, 15% in 2022-24)                           | open                                                                                                         |
| D3  | Force exactly 3 podiums per race in predictions? | Yes (top 3 per race) · no (fixed threshold) | A plain threshold can predict 0 or 6 podiums in one race                              | open                                                                                                         |

### E. Grid and qualifying features

| #   | Decision                                                    | Options                                                                | Why it matters                                                                      | Decided                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| --- | ----------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| E1  | What `grid = 0` means as a feature                          | Last place · empty · separate pit-lane flag                            | Before 1995 it means "never started"; from 2015 it means a pit-lane start (72 rows) | **No `grid = 0` rows in the table (follows from C1 = B), no pit-lane flag.** The prediction function treats a given `grid` of 0 as "starts from the pit lane" and uses the last slot of the race; the report states the model never saw this case. Reasoning below.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| E2  | What to do when a race has no qualifying data               | Fill in · use grid instead · drop those seasons · add a "missing" flag | All races before 1994, most races 1996-2002                                         | **No fill and no row dropped in the cleaned table.** The qualifying columns stay empty where qualifying is missing, and **one boolean column `has_qualifying`** says whether the driver has a qualifying row (a qualifying position). Experiments filter on it (X1, X2) or fill the empty values (X5) in step 10. Reasoning below.                                                                                                                                                                                                                                                                                                                                                        |
| E3  | How to use `q2` / `q3` when empty                           | "Knocked out" flag · use best available time                           | Empty means "knocked out" from 2005/2006, but "session did not exist" before that   | **Not filled in.** The three times become one number: the driver's best qualifying time (from whichever of `q1`-`q3` exists). (Missing values → `qualifying`) **Note (step 10):** whether the one number should be the best of `q1`-`q3` or the `q1` time only is an experiment (see below); in the cleaned table all three times are kept in seconds.                                                                                                                                                                                                                                                                                                                                    |
| E4  | How to compare lap times between races                      | Raw seconds · gap to pole (seconds or %)                               | Every track has a different lap length, so raw times are not comparable             | **Partly decided:** compare the best time with the fastest driver in that race (gap to pole). Seconds or % still **open**. (Missing values → `qualifying`) **Data check:** across the 27 circuits with at least 5 races (2003+), the pole time correlates +0.59 with the typical gap in seconds and -0.06 with the typical gap in percent (shortest lap, 66 s: 1.07 s = 1.66%; longest, 108 s: 1.87 s = 1.75%), so percent is comparable across circuits and seconds are not. 23 rows (0.26%) have a gap above 20%, none a podium; the 99th percentile is 13.17%. The unit and a cap at the 99th percentile of the training years are compared in step 10; both gaps are built in step 8. |
| E5  | Use qualifying position, grid, or both?                     | One · both · their difference                                          | They match in only 77% of rows (penalties)                                          | **Use both, as two separate feature groups: the grid position and the qualifying position.** Reasoning below.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| E6  | Which team ID to trust when qualifying and results disagree | Results · qualifying                                                   | 10 rows in 2015: "Marussia" in qualifying vs. "Manor Marussia" in results           | **The team comes from `results.constructorId`** (same row as the grid, B2); `qualifying.constructorId` is not used. Reasoning below; code in the notebook ("E6: which team do we trust...").                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |

#### Why E5: the grid position and the qualifying position are two feature groups

Both are known before the race, so neither is leakage. Numbers are for rows with a grid slot after the row filters (E5 itself does not depend on the training window, see point 3).

**Status of the model scores below:** they come from a quick exploratory check made during cleaning (a simple two-feature model). They are **preliminary** and will be repeated as the feature-group ablation in step 10. The decision (two groups) also rests on points 2, 4 and 5, which do not need a model.

| Fact (2003 onward)                       | Value                                           |
| ---------------------------------------- | ----------------------------------------------- |
| Rows with a grid slot                    | 8,884                                           |
| Rows with a qualifying position          | 8,863 (99.8%); the 21 without it have no podium |
| Grid equals qualifying position          | 73.0%                                           |
| Grid ahead of qualifying (moved forward) | 21.2%                                           |
| Grid behind qualifying (moved back)      | 5.8%                                            |
| Before 2004 (EDA 6)                      | 98.4% equal                                     |

**Evidence that the qualifying position adds something beyond the grid.** PR-AUC of a simple logistic model (illustrative: two features, and the split K1 is still open), grid alone against grid plus qualifying position:

| Validation seasons                         | Grid only | Qualifying only | Both  | Both minus grid (95% by races) |
| ------------------------------------------ | --------- | --------------- | ----- | ------------------------------ |
| 2020-2021 (117 podiums), trained 2003-2019 | 0.639     | 0.655           | 0.662 | +0.025 (+0.005 to +0.053)      |
| 2017-2019 (186 podiums), trained 2003-2016 | 0.700     | 0.685           | 0.707 | +0.007 (+0.001 to +0.014)      |
| 2013-2016 (234 podiums), trained 2003-2012 | 0.659     | 0.660           | 0.667 | +0.008 (+0.002 to +0.015)      |

**Reasons**

1. **Both together beat the grid alone in all three validation windows,** and neither alone is clearly better (qualifying alone is slightly better in two windows and slightly worse in one). The gain is small (+0.007 to +0.025 PR-AUC).
2. **They carry different information.** The grid is where the car starts after penalties; the qualifying position is how fast the driver was. They differ in 27.0% of the rows from 2003 on, and the grid is ahead of the qualifying position in 21.2% of them.
3. **The result does not depend on the training window (C4).** With the qualifying position filled with the grid position where it is missing, the gain is the same whether training starts in 1950, 1994 or 2003 (+0.023 for validation 2020-2021 and +0.007 for 2017-2019 in every case). The only rows that carry information about the difference are those where the two differ, and all of them are from 2004 or later; older rows only say "equal".
4. **The brief asks for it.** The feature-group ablation lists groups such as "standings, qualifying, grid"; keeping grid and qualifying as separate groups lets us report what each contributes.
5. **Qualifying only was rejected:** it ignores penalties, which are real and known before the race, and it has missing values (21 rows from 2003 on) that the grid does not.

**Limits (state in the report):** the gain is small, and in 2017-2019 with training from 1950 the range touches zero (-0.002 to +0.015); the check used a simple two-feature model, so it cannot tell training windows apart (it says nothing about C4); and the two columns are strongly related (73% equal), so their individual importances in SHAP and permutation importance should be read together, not separately.

**Not decided here:** E2, how to fill the qualifying position when it is missing (the check above used the grid position as the fill); E4, how to turn the qualifying times into a gap feature (seconds or percent).

#### Why E2: leave qualifying empty and add a boolean `has_qualifying`

Qualifying is joined onto the results rows by `raceId` + `driverId` (every one of the 10,494 qualifying rows finds its result row; 14,245 result rows have no qualifying row). Counts are for the table after the row filters (24,652 rows).

| Situation                                                                                  | Rows                | Podium rows | `has_qualifying` |
| ------------------------------------------------------------------------------------------ | ------------------- | ----------- | ---------------- |
| 1. The race has no qualifying at all (12,424 up to 1993, 1,790 in 1994-2002)               | 14,214              | 1,862       | False            |
| 2. The race has qualifying, but this driver has no row (mean grid 22.1)                    | 31                  | 0           | False            |
| 3. The driver has a row and a position but no Q1 time (none has `q2`/`q3`; mean grid 18.8) | 145                 | 10          | True             |
| 4. Complete (row and Q1 time)                                                              | 10,262              | 1,472       | True             |
| **`has_qualifying` True / False**                                                          | **10,407 / 14,245** |             |                  |

From 2003 on: 8,863 rows True (8,749 complete, 114 without a Q1 time), 21 rows False.

**Definition chosen:** `has_qualifying` is True when the driver has a qualifying row (a qualifying position). A missing Q1 time (situation 3) is shown by the empty time columns, not by this flag. Empty `q2` / `q3` are never "missing" (they mean knocked out, E3).

**Reasons**

1. **Cleaning does not invent data.** A fill needs a rule learned from training data only (L1), which belongs to preprocessing, and filling the qualifying position with the grid would make the two feature groups of E5 overlap in the table.
2. **No rows are lost,** so the table stays one row per driver per race (24,652 rows), and the rule does not depend on the split or on the training window.
3. **The window and the fill are experiments.** X1 (which seasons, including "only rows with qualifying") is a filter on this column plus the year; X5 (empty against filled) needs the empty values to be there; X2 (with or without qualifying) needs the columns as they are.
4. **One boolean is enough.** Everything else is already visible: empty time columns show a missing time, and the year shows a race with no qualifying data. Situations 1 and 2 can be told apart, if needed, by checking whether any row of the same race has qualifying.

**Limit:** situation 3 contains 10 podium rows, so "has a row but no time" must not be treated as "no chance"; the time columns are simply empty for those rows.

**Not decided here:** the fill rule (experiment X5).

#### Why E6: the team comes from the results table

| Measure                                                        | Value                                                                                                                                                        |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Qualifying rows with a result row for the same driver and race | 10,494 of 10,494                                                                                                                                             |
| Rows where the team differs                                    | **10 (0.10%)**, all in 2015, 5 races: qualifying says `Marussia` (ID 206), results say `Manor Marussia` (ID 209)                                             |
| Results table, 2015                                            | one ID (209) in all 18 rounds, 36 rows                                                                                                                       |
| Qualifying table, 2015                                         | ID 209 in most rounds, but the old ID 206 in rounds 11, 15, 16, 17, 18 (inconsistent inside one season)                                                      |
| Same drivers and car numbers in rounds 10, 11, 12              | Merhi (98) and Stevens (28); only the team ID in `qualifying` changes in round 11 (206 instead of 209), then changes back                                    |
| Rows with a different team are stored together                 | `qualifyId` 6522-6523, 6601-6602, 6620-6621, 6640-6641, 6660-6661 (both cars of the team, per race)                                                          |
| Old ID elsewhere in 2015                                       | `constructor_results` has 4 rows with ID 206 (rounds 11, 15, 17, 19), each next to a row with ID 209 in the same race; `constructor_standings` uses only 209 |

1. **Same row as the grid (B2):** grid and team both come from the kept result row, so they describe one entry.
2. **The results table is consistent;** the qualifying table flips between two IDs in 5 of the 18 rounds of the same season.
3. **It is the same entry in both tables:** same drivers and car numbers, only the label differs; the pattern (both cars, per race, also in `constructor_results`) points to a label that was not replaced, not a real team change.
4. **Nothing needs repair:** the qualifying columns we keep are `raceId`, `driverId`, `position`, `q1`-`q3` (A4), joined on `raceId` + `driverId`, where all 10,494 rows find their result row. The 10 rows keep the right team.
5. **Tiny:** 10 of 10,494 qualifying rows (0.10%), one season.

**Not decided here:** whether `Marussia` (206, last rows in 2014) and `Manor Marussia` (209, first rows in 2015) are one team for the team-form feature (G3).

### F. Standings before the race

| #   | Decision                                                 | Options                                          | Why it matters                                                                                              | Decided                                                                                                                                                                                                                        |
| --- | -------------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| F1  | How to find "the previous race"                          | Same season, `round - 1` · by date               | `year` + `round` is unique, so this is safe                                                                 | **B: the previous race is the race with the latest date before this race's date** (taken from all races in `races`; the standings used are the rows of that `raceId`). Reasoning below.                                        |
| F2  | What to use for round 1                                  | 0 · last season's final standings · empty        | Round 1 has no earlier race in the season (1,738 result rows)                                               | **Follows from F1 = B: round 1 takes the final standings of the previous season** (the standings after the last race of the previous season). The scale difference is handled under F5, new drivers under F3. Reasoning below. |
| F3  | What to use when a driver has no earlier row this season | 0 · empty                                        | 1,490 of 3,211 driver-seasons start after round 1 (new or replacement drivers)                              | **No standings row means 0 points** (`points_before` is filled with 0 for the 1,577 rows). Reasoning below; code in the notebook ("Standings before the race (decisions F1, F2 and F3)").                                      |
| F4  | Team standings before 1958                               | Empty · drop those seasons                       | The constructors' championship started in 1958 (64 races without it)                                        | **Leave the team standings empty before 1958** (the Constructors' Championship did not exist). Whether this case is used depends on the training window (C4 / X1) and the split (K1). Reasoning below; code in the notebook ("Team standings before 1958 (decision F4)"). |
| F5  | How to compare points across eras                        | Raw points · rank · share of the leader's points | A win was worth 8-10 points before 2010 and 25 after; Abu Dhabi 2014 gave double points (50)                | **Do not use raw points; build a relative measure.** Two versions are built in step 8, the **rank** in the standings and the **share of the leader's points**; which one is used is experiment X6 (step 10). Reasoning below. |
| F6  | How to treat special standings labels                    | Ignore · treat as last                           | `positionText` has `D` (1 driver row) and `E` (17 team rows): disqualified / excluded from the championship | **Ignore `positionText`; use `position`**, which is always a number. (Formats → `driver_standings`, `constructor_standings`)                                                                                                   |

#### Why F1 = B (and F2 by consequence): the previous race is the nearest earlier race by date

**Why a previous race is needed.** A standings row is the table _after_ a race and includes that race's points (e.g. a driver's 2008 standings: 10 points after round 1 = the 10 he scored; 14 after round 2 = 10 + 4; checked on the data: the standings equal the running total including the race itself in 96.7% of the rows, against 67.9% for the total without it, and the latter is almost all drivers who scored 0). Using the standings of the race being predicted would be leakage, so the rows of the race before it are used.

| Check                                                        | Result                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------- |
| `(year, round)` unique across the 1,125 races                | yes                                                                 |
| Rounds of a season are exactly 1, 2, ... n                   | all 75 seasons                                                      |
| Date order equals round order; no two races share a date     | all 75 seasons                                                      |
| Days between consecutive races                               | minimum 1, median 14, maximum 149                                   |
| Races with driver standings                                  | 1,125 of 1,125 (constructor standings: 1,061, none before 1958, F4) |
| Days from the last race of a season to the first of the next | 57 to 266, median 133                                               |

**Reasons for B**

1. **Inside a season it changes nothing:** "round − 1" and "nearest earlier date" give the same race for every round from 2 on, in all 75 seasons.
2. **It is one rule for every row,** with no special case for round 1 (which "round − 1" would leave without a previous race).
3. **Round 1 gets information that exists.** Round 1 is 1,612 rows (6.5% of the table; 455 from 2003 on). 84% of them (82% from 2003 on) belong to a driver with a final standing from the previous season. Exploratory check (no model): on the 374 round-1 rows from 2003 on with a previous standing, last season's final rank alone has PR-AUC 0.491 against a podium rate of 17.1% (no-skill level), and a rank correlation of 0.57 with the grid; the grid alone has 0.637. So it is informative, though weaker than the grid.
4. **The rule uses the `races` table, not our filtered table,** so the race after one that was removed (for example the Indianapolis 500, C3) still finds its previous race, whose standings exist.

**Example (Hamilton, 2009):** points before the race are 98 (round 1: the 2008 final), 0 (round 2: he was disqualified in round 1, scored 0 and has no standings row), 1, 4, 9 (rounds 3 to 5).

**Consequences to handle (not decided here)**

- **Scale (F5):** round 1 gets a full-season total (98) while round 2 gets a few races' worth (0, 1, 4, 9). The points must be put on a comparable scale (rank, or share of the leader's points).
- **No standings row (F3):** 469 result rows (1.8%) have no standings row for that race; all of them scored 0 points in it, mostly in the 1990s (297) and 2000s (150), in rounds 1-3. A missing row is read as "no points yet". Also, 16-18% of round-1 rows are new drivers with no previous standing.
- **Team standings** follow `constructorId`; renames and the years before 1958 are G3 and F4.

**Limit:** last season's standing at round 1 describes a car and a line-up from before the winter break (133 days earlier on median); it is a weaker signal than at later rounds.

#### Why F3: no standings row means 0 points

Counts are for the table after the row filters (24,652 rows), with the previous race from F1 = B.

| State of the driver at the previous race                        | Round 1 | Later rounds | Total          | Podium rate |
| --------------------------------------------------------------- | ------- | ------------ | -------------- | ----------- |
| A. Has not started yet in that season (grid slot = started, C2) | 263     | 906          | **1,169**      | 2.8%        |
| B. Has started, 0 points so far                                 | 2       | 406          | **408**        | 6.6%        |
| C. Has points but no standings row                              | 0       | 0            | **0**          |             |
| Rows with a standings row                                       |         |              | 23,075 (93.6%) | 14.2%       |

By era (rows without a standings row): 913 before 1990 (900 A, 13 B), 440 in 1990-2002 (123 A, 317 B), 224 from 2003 on (146 A, 78 B; 2.5% of 8,884 rows). Where a row exists (round 2 onward), the standings points equal the running total of the race points in 96.6% of the rows.

1. **0 is the true value in every case:** a driver who has not started cannot have points, and one who started and scored nothing has 0; no row has points without a standings row (state C = 0).
2. **The standings behave as a running total,** so a driver with nothing to add is simply not listed.
3. **Empty would say "unknown" where the value is known** and would need a fill later (learned from training data only).
4. **The difference between A and B is kept elsewhere:** podium rates differ (2.8% / 6.6% / 14.2%), and the number of races started so far this season (0 for A, 1 or more for B) is a form feature (group G); no flag is added here.
5. **Small and mostly old:** 6.4% of the rows.

**Limits:** "has started" means "has a grid slot" (C2); in 3.4% of the rows with a standings row the points differ from the running total and the cause was not examined; the rank of a driver with 0 points is F5.

#### Why F4: team standings are left empty before 1958

| Fact | Value |
|---|---|
| First season of `constructor_standings` and of `constructor_results` | 1958 (the introduction: Constructors' Championship "since 1958") |
| Races without team standings | 64: exactly the 1950-57 races (7, 8, 8, 9, 9, 7, 8, 8) |
| Driver standings | all 1,125 races |
| Rows with no team standings at the previous race | **1,182** (4.8%): 1,172 in 1950-57, 10 in round 1 of 1958; podium rate 14.6% |
| Rows with a team standings row | 22,994 (93.3%), podium rate 13.7% |
| Rows where standings exist but not for this team | 476 (1.9%), podium rate 4.0%; in 474 the team had 0 points so far (`constructor_results`), in 2 it had points |
| Rows from 2003 on with no team standings | 0 of 8,884 |

1. **The value does not exist:** no team championship, so the standing is missing, not zero. A 0 would say "the team had 0 points", which is false, and would mix two meanings of 0 in one column.
2. **It keeps every row,** as in E2; the old seasons are a window choice, not a cleaning rule.
3. **Models can see it as missing,** and "team standing available" is information in itself.
4. **Team form for 1950-57 is still possible** from the results (group G); this decision is only about the standings table.

**The window and the split decide whether this is used:** the rule is for the cleaned table, which keeps all seasons. A window starting in 1958 or later meets the case only in round 1 of 1958 (10 rows); a window starting in 2003 or later never meets it (0 of 8,884 rows); a window that includes 1950-57 meets it for 1,172 rows (4.8%) and the team-standings features must cope with missing values (a point for the feature-group ablation). This is settled by the experiments X1 and the split K1.

**Not decided here:** the 476 rows of state 3 (a team without a row after 1958); in 474 the team had 0 points so far, the same reading as F3 for drivers, to be confirmed.

#### Why F5: no raw points; rank and share are built, and compared in step 10

Descriptive evidence only (no scores): raw points mean different things in different eras and at different rounds.

| Fact (from the data) | Value |
|---|---|
| Points for a win (largest race points in a race) | 5-9 (1950s), 9 (1960s-80s), 10 (1990s-2000s), 25 (2010s; 26 with a bonus; 50 once, Abu Dhabi 2014), 25 (2020s) |
| Leader's final total, median by decade | 35 (1950s), 46, 63, 72, 96, 116, 384 (2010s), 437 (2020s; maximum 575) |
| Season length | 7 to 24 rounds |
| Leader's points in 2019 after round 1 / 5 / 10 | 26 / 112 / 223 |
| Races where the leader has 0 points in the standings | 0 of 1,125 (a share of the leader's points is always defined) |
| Round 1 (F1 = B) | uses the last season's final total (e.g. 98), round 2 uses one race's worth (e.g. 0 or 10): the same column changes scale |

**Reasons**
1. **Raw points are not comparable** across eras (a win is worth 8-10 points, then 25; the leader's final total is about twelve times larger in the 2020s than in the 1950s), across rounds of one season (26 to 223), and between round 1 and round 2 under F1 = B.
2. **A relative measure says "where in the table"** instead of "how many points", so the same number means the same thing in every era and round.
3. **The two relative measures differ in structure, not in a score:**

| | Rank | Share of the leader's points |
|---|---|---|
| Needs an invented value for a driver with no standings row (F3 = 0 points) | yes (e.g. listed drivers + 1) | no: 0 points = share 0 |
| Keeps how far behind a driver is | no | yes |
| Depends on how many drivers are listed (varies by era) | yes | no |
| Ties | possible (broken by wins) | none needed |

4. **Both are built, neither is chosen now,** as with the two gap versions in E4; the comparison is an experiment (X6).

**Note on evidence:** an earlier exploratory comparison of each measure alone against the podium label (ROC-AUC, no model fitted) is **not** used as evidence for this decision, because predictive comparisons belong to the modeling phase. If used at all, it only points to what to expect in X6.

**Not decided here:** how the rank is defined for a driver with no standings row (needed only if the rank version is kept after X6).

### G. Recent-form features (from past races only)

| #   | Decision                                                   | Options                                                         | Why it matters                                                              | Decided |
| --- | ---------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------- | ------- |
| G1  | How many past races to look at                             | Last N races · season so far · whole career                     | Short windows react fast but are noisy                                      | **Build five windows: the last 3, the last 5, the last 10 races, the season so far, and the whole career** (only earlier races). Which one is used is experiment X7 (step 10). Reasoning below. |
| G2  | Driver form, team form, or both                            | —                                                               | The car usually matters more than the driver                                | **Build both: driver form and team form, as two feature groups** (each with the windows of G1, earlier races only). Reasoning below; code in the notebook ("Driver form and team form (decision G2)"). |
| G3  | Follow teams through renames?                              | Use `constructorId` (history resets) · build a team-lineage map | Toleman → Benetton → Renault → Lotus → Alpine; Toro Rosso → AlphaTauri → RB | **Follow `constructorId`; a rename resets the team's history.** A lineage table is an optional step 10 experiment (X8). Reasoning below. |
| G4  | Which team's form for a driver who changed team mid-season | Current team · previous team                                    | Common in the 1960s (17% of drivers), rare today (2%)                       | **The current team** (the team the driver races for in this race). Reasoning below; code in the notebook ("The team form of a driver who has changed team (decision G4)"). |
| G5  | What to use for a driver's first race (no history)         | 0 · empty · average                                             | Every driver has a debut (861)                                              | **Empty when there is no earlier start; a window with only some history uses the races that exist.** The fill, if any, is a step 10 preprocessing choice. Reasoning below; code in the notebook ("A driver's first start: no history (decision G5)"). |
| G6  | Reset form at the start of each season?                    | Reset · carry over                                              | Cars change a lot between seasons                                           | open    |
| G7  | Which past results to measure                              | Podium rate · average finish · points · DNF rate                | Each tells a different story                                                | open    |
| G8  | Do past non-starts count in form?                          | Count · skip                                                    | A "did not qualify" is not a race result                                    | open    |
| G9  | Add circuit history (driver at this track)?                | Yes · no                                                        | Few races per driver per circuit, so it is noisy                            | open    |
| G10 | Add the year or era as a feature?                          | Yes · no                                                        | Podium patterns change by era                                               | open    |

#### Why G1: five windows are built, and chosen by experiment

Counts are for the table after the row filters (24,652 rows; 8,884 from 2003 on). "Earlier starts" are starts (grid slot, C2) of the same driver before this race.

| Fact | All rows | From 2003 on |
|---|---|---|
| Earlier starts of the driver, career (median) | 45 | 81 |
| Rows with fewer than 5 earlier starts (career) | 10.4% | 4.8% |
| First start ever | 2.8% | 1.0% |
| Earlier starts in the same season (median) | 6 | 9 |
| Rows with fewer than 5 earlier starts this season | 41.0% | 28.2% |
| First start of a season (nothing earlier this season) | 10.8% | 5.9% |
| Rounds per season (median) | 16 | 19 |
| Earlier starts of the team (median) | | 391 |
| Rows where the driver changed team since the previous start | | 1.6% |

How far back each window reaches (all rows):

| Window | Days back, median | 90th percentile | Reaches into the previous season |
|---|---|---|---|
| Last 3 starts | 49 | 196 | 21.6% of rows |
| Last 5 starts | 77 | 279 | 34.2% |
| Last 10 starts | 252 | 427 | 63.1% |

**Reasons**
1. **Short windows are current but noisy and have gaps; long windows are stable but mix cars and seasons.** The last 10 starts reach into the previous season for 63% of the rows (another car, other rules); the season so far is short at the start of a season (28% of the 2003+ rows have fewer than 5 earlier races, 5.9% have none); the career is a stable level of the driver but ignores the current car.
2. **The data cannot say which length is best.** Choosing one needs a comparison on the target, which is a modeling-phase experiment (X7, with the feature-group ablation), not a cleaning or feature-definition argument.
3. **Building the candidates costs nothing** and keeps the options open.
4. **Every window uses earlier races only** (the strict rule: shift by one race before any rolling window, grouped by driver or team and sorted by date).

**Not decided here:** driver form, team form or both (G2), what the form measures (G7), and what to use when there is no history (G5, G6, G8).

#### Why G2: driver form and team form, as two groups

Counts are for the table after the row filters (24,652 rows).

| | 1950-65 | 1966-88 | 1989-2002 | 2003-24 |
|---|---|---|---|---|
| Team-races | 862 | 4,180 | 2,817 | 4,476 |
| One car | 18.9% | 29.5% | 7.9% | 1.5% |
| Two cars | 28.1% | 59.9% | 92.1% | 98.5% |
| Three or more cars | 53.0% | 10.6% | 0% | 0% |
| Rows with a teammate in the same race | 93.8% | 84.1% | 95.9% | 99.2% |
| Driver's team differs from his previous start | 16.3% | 7.1% | 3.5% | 1.8% |
| of which within the same season | 7.8% | 2.2% | 0.5% | 0.2% |
| Rows with fewer than 10 earlier races of the team | 32.3% | 10.1% | 4.7% | 4.7% |
| Driver was also in the team's previous race | 65.9% | 86.8% | 92.6% | 96.4% |

(Earlier chat figures for "earlier starts of the team" counted cars, not races, and were lower; these count the team's earlier races.)

**Reasons for building both**
1. The car matters most (the introduction, an allowed source), and the team form measures it; from 2003 on a team has two cars in 98.5% of its races, so twice the past results of one driver.
2. The driver form measures the person and tells two drivers of the same team apart (a teammate exists for 99.2% of the rows from 2003 on; both would otherwise have the same team value).
3. Two groups can be reported separately in the feature-group ablation.
4. Each covers the other's weak case: the driver form works for one-car teams and young teams; the team form works for a driver who has just changed team.

**Rejected**
- **A. Driver only:** ignores the car, has half the data of a two-car team, and for a driver who changed team (1.8% of rows from 2003 on) his past describes another car.
- **B. Team only:** the two drivers of a team would get the same value; the team is badly defined in the early periods (53.0% of 1950-65 team-races have three or more cars, 18.9% one; 29.5% of 1966-88 team-races have one); a new team has little history (32.3% of 1950-65 rows have fewer than 10 earlier team races); it already contains the driver's own results.
- **D. Driver form plus teammate-only form:** needs a teammate in the same race (missing for 0.8% of rows from 2003 on, 4.1% in 1989-2002, 15.9% in 1966-88, 6.2% in 1950-65) and adds a third construction for an overlap not shown to matter; a possible refinement in step 10.

**Limit (state in the report):** the groups overlap (96.4% of rows from 2003 on have the driver in the team's previous race), so their importances in the ablation and in SHAP must be read together.

**Not decided here:** renames (G3), the team of a driver who changed team (G4), what the form measures (G7).

#### Why G3: follow `constructorId`, renames reset the history

| Fact | Value |
|---|---|
| Constructor IDs in the table | 212 IDs, 167 with at least one row; 54 span one season, 43 span 2-3 seasons, 70 span four or more |
| Candidate renames found from the data alone (a new ID starts as another stops, with a driver in common) | 52 in all years, 22 from 2003 on; they include wrong ones (e.g. `Lotus F1` → `Haas F1`, a driver who moved) |
| Examples that look like real renames | Force India (10, 2008-18) → Racing Point (211, 2019-20); Toro Rosso (5, 2006-19) → AlphaTauri (213, 2020-23) → RB F1 Team (215, 2024); Virgin (166) → Marussia (206) → Manor Marussia (209) |
| Identity in the dataset is inconsistent | `Renault` (ID 4) spans 1977-2020 (401 races), while the introduction's chain "Toleman became Benetton, then Renault, Lotus, Alpine" has separate IDs: Toleman 53 (1981-85), Benetton 22 (1986-2001), Lotus 205 (2010-11), Lotus F1 208 (2012-15), Alpine 214 (2021-24) |
| Rows whose team ID has fewer than 10 earlier races | 2,300 of 24,652 (9.3%); from 2003 on 415 of 8,884 (4.7%) |
| Of those 415, in an ID with a data-based predecessor candidate | 346 (at most 3.9% of the 2003+ rows; an upper bound: it includes wrong candidates and genuinely new teams) |

**Reasons**
1. **The introduction asks for it** (an allowed source): "A 'constructor form' feature must follow constructorId, and we should accept that renames reset history."
2. **The effect is small and limited to the first races of a new ID** (at most 3.9% of the rows from 2003 on).
3. **The data cannot give a reliable lineage.** Driver continuity finds real renames and wrong ones, and the IDs themselves are inconsistent (one `Renault` ID over 1977-2020, separate IDs for the other names of the introduction's chain). A lineage table would need outside knowledge, as the nine nationality links did in I1, and a wrong link would give a team the past of another team.
4. **It keeps the rule simple and the same for every row.**
5. `Marussia` (206) and `Manor Marussia` (209) stay two teams (consistent with E6).

**Rejected:** B, a lineage table (outside knowledge, risk of wrong links); C, merging only the renames named in the introduction (a half-way table, and the dataset's IDs for that chain are already inconsistent).

**Limit (state in the report):** after a rename the team form starts empty for the first races of the new ID, so the first few races of such teams rely on the driver form.

**Not decided here:** the team form of a driver who has changed team (G4), and what to use when there is no history (G5, G6, G8).

#### Why G4: the team form is the form of the current team

Counts are for the table after the row filters; 23,963 of the 24,652 rows have a previous start.

| Period | Rows with a previous start | Team changed since the previous start | Share | Of which within the same season |
|---|---|---|---|---|
| 1950-65 | 2,322 | 378 | 16.3% | 143 |
| 1966-88 | 7,520 | 536 | 7.1% | 153 |
| 1989-2002 | 5,326 | 189 | 3.5% | 25 |
| 2003-24 | 8,795 | 156 | 1.8% | 14 |
| **All** | **23,963** | **1,259** | **5.3%** | **335** |

| Rows with a team change | Value |
|---|---|
| Podium rate (other rows) | 6.3% (14.3%); from 2003 on 7.1% |
| The new team has fewer than 10 earlier races | 30.7% (other rows: 7.4%) |
| The previous team also takes part in this race | 62.0% (so 38.0% not) |

**Reasons**
1. The prediction is about this race, so the car that matters is the one he drives now; his team is known before the race (the qualifying row, E6).
2. His own past in the old car stays in the **driver form** (G2), so the two groups cover two things: the car he has now and his own record.
3. The previous team would describe a car he has left, and for 38.0% of these rows that team is not even in the race.
4. The affected share is small: 5.3% of all rows, 1.8% from 2003 on.

**Rejected:** the previous team.

**Limit:** the current team's history can be short (fewer than 10 earlier races for 30.7% of the rows with a change); what to use when there is no history is G5, G6, G8.

#### Why G5: no history gives an empty form value

| | All years | 2003 on |
|---|---|---|
| Rows | 24,652 | 8,884 |
| First start ever | 689 (2.8%) | 89 (1.0%) |
| Podium rate of those rows (of all rows) | 2.3% (13.6%) | 2.2% (14.5%) |
| Average grid of those rows (of all rows) | 17.5 (11.8) | 16.4 (11.0) |
| Fewer than 3 / 5 / 10 earlier starts | 6.9% / 10.4% / 17.9% | 2.9% / 4.8% / 9.3% |

For rows with history (2003 on, at least 3 earlier starts, 8,625 rows): average finishing place of the last 3 starts has median 11.3 (mean 10.9); the podium share of the last 3 has mean 0.148, and 73.2% of the rows have no podium in their last 3 starts.

**Rule:** empty when there is no earlier start; a window with fewer than N earlier races uses the races that exist, and is empty only when there are none.

**Reasons**
1. **0 claims what the data contradicts:** an average place of 0 is better than the winner; a podium share of 0 is indistinguishable from three races without a podium (73.2% of the rows with history).
2. **The average of everyone (about 10.9) says "typical":** first starts are not typical (grid 16.4-17.5, podium about 2%).
3. **The reason is already visible:** the number of earlier starts (0) is the career window of G1; no flag needed.
4. **A fill must be learned from training data only,** so it is a step 10 choice (like X5).

**Rejected:** A (0) and C (the average of everyone).

**Limit:** the models must handle the empty value; only 1.0% of the rows from 2003 on (2.8% of all rows) are affected.

### H. Question 1 (front row → podium, by circuit)

| #   | Decision                                  | Options                           | Why it matters                                       | Decided |
| --- | ----------------------------------------- | --------------------------------- | ---------------------------------------------------- | ------- |
| H1  | Front row by grid, by qualifying, or both | The question asks to compare both | Qualifying exists only from 1994                     | open    |
| H2  | Which years count as "before 2014"        | All years · 1994-2013 · 2003-2013 | A fair comparison needs similar periods              | open    |
| H3  | Minimum races for a circuit to be ranked  | e.g. at least 5 races per period  | 24 circuits were used 3 times or fewer, 11 only once | open    |

### I. Question 2 (home advantage)

| #   | Decision                                        | Options                                                                       | Why it matters                                                                         | Decided                                                                                                                                                                                                                                                                                                   |
| --- | ----------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I1  | How to match nationality to country             | Write a mapping table                                                         | "British" → "UK", "American" → "USA", "Monegasque" → "Monaco", "Dutch" → "Netherlands" | **Explicit table of 25 links: 16 by spelling + 9 by knowledge** (British→UK, French→France, American→USA, Spanish→Spain, Australian→Australia, Austrian→Austria, Dutch→Netherlands, Swiss→Switzerland, Monegasque→Monaco). Reasoning below; code in the notebook ("The home race (decisions I1 and I2)"). |
| I2  | Dual and historical nationalities               | Pick one country · count both · drop                                          | "American-Italian", "Argentine-Italian", "East German", "Rhodesian"                    | **A race is a home race if the circuit is in the country of either nationality** (2 drivers, 3 rows). Reasoning below.                                                                                                                                                                                    |
| I3  | Merge `USA` and `United States`                 | Yes                                                                           | Same country under two labels                                                          | **Merged to `USA` in A5** (the only `United States` circuit is Las Vegas Strip, 0 km from a circuit labelled `USA`).                                                                                                                                                                                      |
| I4  | How to control for starting position            | Compare within grid groups (e.g. 1-3, 4-6...) · logistic regression with grid | The brief requires this control                                                        | **Compare home and away inside grid bands (1-3, 4-6, 7-10, 11-15, 16+), pooled with the Mantel-Haenszel odds ratio; interval from resampled races.** Reasoning below; code in the notebook ("Question 2: controlling for the starting position (decision I4)").                                           |
| I5  | Drivers from countries that never hosted a race | Exclude · keep as "never home"                                                | e.g. Finnish, New Zealander, Danish, Irish, Colombian drivers                          | **Keep them; `home race` is filled with False ("never home").** 15 nationalities, 46 drivers, 2,344 rows (9.5%). Reasoning below.                                                                                                                                                                         |

#### Why I1 and I2: building the home race

There is **no column** that says home race (checked in all 14 tables: the only place columns are `circuits.location` and `circuits.country`, the only nationality columns are in `drivers` and `constructors`). A race is a home race when the circuit's country is the country of the driver's nationality.

Counts are for the table after B1, C1, C3, C6 and C7 (24,652 rows), with the labels cleaned in A5 (42 driver nationalities, 34 circuit countries).

| Link                                                      | Count | Which                                                                                                                                                                    |
| --------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| By spelling                                               | 16    | Argentine, Belgian, Brazilian, Canadian, Chinese, German, Hungarian, Indian, Italian, Japanese, Malaysian, Mexican, Portuguese, Russian, South African, Swedish          |
| By knowledge (not from the data)                          | 9     | British→UK, French→France, American→USA, Spanish→Spain, Australian→Australia, Austrian→Austria, Dutch→Netherlands, Swiss→Switzerland, Monegasque→Monaco                  |
| No country with a circuit                                 | 15    | Chilean, Colombian, Czech, Danish, East German, Finnish, Indonesian, Irish, Liechtensteiner, New Zealander, Polish, Rhodesian, Thai, Uruguayan, Venezuelan (decision I5) |
| Dual nationality                                          | 2     | American-Italian (Thiele), Argentine-Italian (de Tomaso) (decision I2)                                                                                                   |
| Countries with circuits but no driver of that nationality | 9     | Azerbaijan, Bahrain, Korea, Morocco, Qatar, Saudi Arabia, Singapore, Turkey, UAE                                                                                         |

**Why an explicit table (I1)**

1. No column exists, so the link has to be built.
2. Spelling alone finds 16 of the 25 links and 1,006 of the 1,937 home rows; the nine knowledge links add 931 rows (48%): UK 451, France 207, USA 112, Spain 61, Austria 29, Australia 27, Netherlands 22, Switzerland 13, Monaco 9.
3. The knowledge links are few, listed with their number of drivers and circuits, and marked as knowledge, not as a finding of the data.
4. The code checks that every link points to an existing country and that no nationality is linked twice.
5. A spelling rule alone would link `Argentine-Italian` to Argentina by accident; dual nationalities are therefore left out of that step.

**Why "either nationality" (I2)**

- 2 drivers, 3 rows, 0 podiums. Counting either nationality gives 2 home races (Thiele, Italy 1960; de Tomaso, Argentina 1957); the first-listed nationality only gives 1.
- It is the same definition of home as for everyone else, applied to each nationality the driver holds; the order in the label has no meaning in the data.
- The effect is at most 2 rows of 24,652 and no podium, so no choice here can change an answer.

**Result:** 1,937 home races with single nationalities, **1,939 (7.9%)** after I2.

#### Why I5: keep the rows with no home country, filled with "never home"

15 nationalities (Chilean, Colombian, Czech, Danish, East German, Finnish, Indonesian, Irish, Liechtensteiner, New Zealander, Polish, Rhodesian, Thai, Uruguayan, Venezuelan) have no country with a circuit. They are 46 drivers and **2,344 rows (9.5%)**. (The 2,347 rows quoted earlier also counted the 3 rows of the 2 dual drivers, handled in I2.)

| Group                                      | Drivers | Rows   | Share | Podium rows | Podium rate (grid **not** controlled) |
| ------------------------------------------ | ------- | ------ | ----- | ----------- | ------------------------------------- |
| Home race                                  | 502     | 1,939  | 7.9%  | 225         | 11.6%                                 |
| Away race (home country has a circuit)     | 533     | 20,369 | 82.6% | 2,756       | 13.5%                                 |
| **Never home (no country with a circuit)** | 46      | 2,344  | 9.5%  | 363         | 15.5%                                 |

1. **They are valid away-race observations**, with the same row rules, grid and label as everyone else; dropping them removes 9.5% of the rows without a reason from the data.
2. **The label is exact:** none of the 34 circuit countries is theirs, so "not a home race" is true, not a guess. None of these rows is marked as home.
3. **They help the control for the grid (I4):** the grid-podium relation is learned from all rows.
4. **Dropping them would not change the home group** (0 home rows); it would only shrink the away group.

**Risk (state in the report):** they are a different population (e.g. Finnish drivers, 1,152 rows) with a higher podium rate than the other away rows, so they raise the "away" rate in a plain home-against-away comparison. The column `home possible` separates the two kinds of away rows; Question 2 reports them separately or compares each driver's home races with that same driver's away races (I4).

#### Why I4: compare inside grid bands

Counts are for the table after the row filters (24,652 rows, 1,939 home races).

| Measure                | Home  | Away   |
| ---------------------- | ----- | ------ |
| Rows                   | 1,939 | 22,713 |
| Podium rate (raw)      | 11.6% | 13.7%  |
| Average starting place | 12.7  | 11.7   |

The starting place matters a great deal by itself: podium rate 55.4% from places 1-3, 26.1% (4-6), 9.1% (7-10), 2.9% (11-15), 0.7% (16+). So the raw gap (-2.1 points) cannot be read as a home effect.

| Grid band | Home rows | Home podium % | Away rows | Away podium % | Difference (points) |
| --------- | --------- | ------------- | --------- | ------------- | ------------------- |
| 1-3       | 231       | 55.8          | 3,111     | 55.4          | +0.5                |
| 4-6       | 226       | 26.5          | 3,117     | 26.0          | +0.5                |
| 7-10      | 337       | 7.1           | 4,117     | 9.2           | -2.1                |
| 11-15     | 415       | 2.4           | 5,126     | 3.0           | -0.6                |
| 16+       | 730       | 0.3           | 7,242     | 0.7           | -0.5                |

**Pooled (Mantel-Haenszel) odds ratio 0.93, 95% range 0.78-1.07 (300 resamples of races); weighted difference -0.5 points** (against -2.1 without the control).

**Why this method (A)**

1. It is what the brief describes: "comparing drivers who started from similar grid positions".
2. The control works: inside every band home and away drivers start from almost the same average place (1.95 / 2.00, 5.03 / 4.99, 8.56 / 8.49, 12.99 / 12.99, 20.15 / 19.69).
3. The result does not depend on the band edges: odds ratio 0.93 (our 5 bands), 0.94 (3 bands), 0.93 (8 bands), 0.93 (each grid place alone).
4. It agrees with other controls: band and era together 0.91 (45 cells, 3 with fewer than 10 home rows); logistic regression on home, grid place and era 0.96.
5. It is easy to show and explain: five comparisons, then one pooled number.

**Alternatives not used as the main method:** a logistic regression (one number and interval, assumes a smooth effect of the grid, harder to explain) and a within-driver comparison (392 drivers with both home and away rows, removes driver quality, fewer rows); both are kept as checks.

**Limits (state in the report):** the band edges are our choice (tested); the interval is wide, so a small effect either way cannot be excluded; only the starting place is controlled, not the car or the driver; it describes an association, not a cause.

### J. Question 3 (mechanical failures by team)

| #   | Decision                                | Options                                     | Why it matters                                                                                                                               | Decided |
| --- | --------------------------------------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| J1  | Which statuses count as "mechanical"    | Write a mapping for all statuses that occur | 62 different statuses appear in 2014-2024; some are unclear: `Retired`, `Technical`, `Damage`, `Collision damage`, `Puncture`, `Out of fuel` | open    |
| J2  | What to divide by                       | Race starts only · all entries              | Drivers who never started cannot fail                                                                                                        | open    |
| J3  | Per `constructorId` or per team lineage | —                                           | Teams were renamed between the two eras                                                                                                      | open    |
| J4  | Minimum starts for a team to be shown   | e.g. 20 starts                              | Teams with very few starts give extreme rates                                                                                                | open    |
| J5  | Count sprint failures?                  | Yes · no                                    | Sprints exist only from 2021                                                                                                                 | open    |

### K. Split and evaluation

| #   | Decision                                      | Options                                           | Why it matters                                            | Decided |
| --- | --------------------------------------------- | ------------------------------------------------- | --------------------------------------------------------- | ------- |
| K1  | Confirm the season split                      | Train ≤ 2019 · validation 2020-2021 · test ≥ 2022 | Given in the intro PDF                                    | open    |
| K2  | Main and second metric                        | e.g. PR-AUC main, ROC-AUC second                  | The brief asks us to justify the choice; podiums are rare | open    |
| K3  | How to choose the decision threshold for F1   | Best F1 on validation · top 3 per race            | Must use validation, never test                           | open    |
| K4  | The brief's "all five metrics"                | Add precision, recall, accuracy · ask             | Only three metrics are listed in the brief                | open    |
| K5  | Retrain on train + validation before testing? | Yes · no                                          | More data vs. a cleaner comparison                        | open    |
| K6  | Treat 2020 as a normal season?                | Yes · note it                                     | COVID season: only 17 races                               | open    |

### L. Preprocessing and models

| #   | Decision                                  | Options                                                                             | Why it matters                                        | Decided |
| --- | ----------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------- | ------- |
| L1  | How to fill missing feature values        | Median · constant · add "missing" flag                                              | Learned on train only, to avoid leakage               | open    |
| L2  | Scale numeric features?                   | Standard · min-max · none                                                           | Needed for logistic regression and the neural network | open    |
| L3  | How to encode IDs (driver, team, circuit) | Drop · one-hot · target encoding                                                    | Target encoding can leak the answer                   | open    |
| L4  | Which two preprocessing orders to compare | e.g. fill-then-scale vs. scale-then-fill; filter before vs. after building features | The brief requires at least two                       | open    |
| L5  | Baseline model                            | e.g. logistic regression                                                            | Required reference point                              | open    |
| L6  | Second statistical model                  | Random forest · gradient boosting                                                   | At least two statistical models required              | open    |
| L7  | Neural network library and size           | PyTorch · Keras · scikit-learn MLP; 1-2 hidden layers                               | Not installed yet                                     | open    |
| L8  | How to tune settings                      | Grid search · random search · manual                                                | Validation set only                                   | open    |
| L9  | Feature groups for the ablation           | e.g. grid · qualifying · standings · form · driver/circuit info                     | Required experiment                                   | open    |
| L10 | Random seed                               | Fix one seed                                                                        | So results can be repeated                            | open    |

### M. Explanations and the prediction function

| #   | Decision                                | Options                              | Why it matters                                     | Decided |
| --- | --------------------------------------- | ------------------------------------ | -------------------------------------------------- | ------- |
| M1  | Which model to explain                  | The best one · all                   | SHAP and LIME take time                            | open    |
| M2  | Which race / driver to explain locally  | A correct podium · a surprising miss | One example is required                            | open    |
| M3  | Input format of the prediction function | Dictionary · one-row table           | Must work with missing values                      | open    |
| M4  | Which incomplete record to demonstrate  | e.g. a row with no qualifying data   | The brief asks for a complete and a partial record | open    |

## Experiments to run in step 10

The brief accepts trial-and-error evidence kept in the notebook. These choices are settled there, with the full features, intervals by race, and one cell or section per attempt, not by argument during cleaning.

| #   | Question                       | Variants to compare                                                                                                                                                                                                                          | Related decision           |
| --- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| X1  | Which seasons to train on      | (a) 2003 onward, 8,884 rows; (b) **1994 onward, only rows with qualifying** (1994-2002: 1,530 rows in 65 races, 195 podium rows; with 2003+: 10,414 rows); (c) 1994 onward, all rows with a fill and a flag (12,228); (d) all years (24,652) | C4                         |
| X2  | Qualifying features: yes or no | With and without qualifying (position, gap), before and after 2003                                                                                                                                                                           | E5, feature-group ablation |
| X3  | One qualifying time            | Best of `q1`-`q3` against `q1` only                                                                                                                                                                                                          | E3                         |
| X4  | Unit of the gap                | Seconds, percent, percent capped at the 99th percentile of the training years                                                                                                                                                                | E4                         |
| X5  | Missing qualifying             | Leave empty (and flag) against fill with the grid position                                                                                                                                                                                   | E2                         |
| X6 | Points on a common scale | Share of the leader's points against rank in the standings (both built in step 8) | F5 |
| X7 | Window of the recent form | Last 3, last 5, last 10 races, season so far, whole career (and the combination) | G1 |
| X8 | Team identity | `constructorId` as it is against a lineage table of renames (only if time allows) | G3 |

**In 1994-2002 the qualifying data is all or nothing per race** (no race has between 0% and 90% coverage), so variant (b) of X1 needs neither a fill nor a flag. The covered races of 1996-2002 are mostly early in the season (74% in rounds 1-8, against 38% of the races without qualifying) but look the same on outcomes (podium rate 13.7% against 13.9%, mean grid 11.5 against 11.3, starters per race 21.9 against 21.5).

**What to expect (exploratory run during cleaning, not evidence):** gradient boosting on grid and field size, with or without qualifying features, PR-AUC on three later validation periods (2020-21, 2017-19, 2013-16).

- Adding qualifying: +0.034, +0.023, +0.019 (every range above zero).
- Dropping 1950-2002 without qualifying: -0.007, +0.028, -0.001 (old years did not help).
- All years with a fill and a flag against 2003+: +0.002, -0.027, +0.011 (no consistent gain).
- `q1` only against best of `q1`-`q3` (logistic model, 2006 onward): +0.018 (range -0.008 to +0.051) and +0.004 (-0.016 to +0.025), so not distinguishable.

**Caveats of that run:** only grid, field size and qualifying features (no form or standings), one model type without tuning, a gap only where at least 90% of the rows of a race have a time, and the split (K1) was still open. Form features can look back before 2003 for rows in a 2003+ window, so a later start does not starve them of history.

---

## Edge Cases to Handle

Concrete situations in our data that the code must deal with. Each one links to the decision above that settles it.

| #   | Edge case                                                                             | Where                      | Count                                                                   | Decision             |
| --- | ------------------------------------------------------------------------------------- | -------------------------- | ----------------------------------------------------------------------- | -------------------- |
| 1   | Same driver appears 2 or 3 times in one race (shared cars)                            | `results`                  | 85 cases, 176 rows (1950-1964)                                          | B1, B2               |
| 2   | One driver listed twice only because he failed to qualify with two teams (Ertl, 1978) | `results`                  | 1 case                                                                  | B1                   |
| 3   | A driver holds two podium places in one race (Farina and Trintignant, 1955 Argentina) | `results`                  | 2 cases                                                                 | B1, B3               |
| 4   | Two drivers credited with the same finishing place (shared car)                       | `results`                  | 228 rows; 18 races with 4-7 podium rows                                 | B3                   |
| 5   | Half or split points from shared cars                                                 | `results.points`           | 42 rows with fractional points                                          | F5, G7               |
| 6   | `grid = 0` meaning "never started"                                                    | `results`                  | Most of 1,638 rows, mainly 1957-1994                                    | C1, E1               |
| 7   | `grid = 0` meaning a pit-lane start                                                   | `results`                  | 72 rows, 2015-2024                                                      | E1                   |
| 8   | Grid slot but 0 laps (out on lap 1)                                                   | `results`                  | 966 rows                                                                | C2                   |
| 9   | "Withdrew" but has a grid slot or laps                                                | `results`                  | 84 with grid, 23 with laps                                              | C2                   |
| 10  | Official `position` differs from `positionOrder` after disqualifications              | `results`                  | 13 rows (1983 Brazilian GP)                                             | D1                   |
| 11  | No qualifying row at all                                                              | `qualifying`               | All races before 1994, most of 1996-2002, plus 59 rows in covered races | E2                   |
| 12  | `q2` / `q3` empty because the session did not exist                                   | `qualifying`               | All rows before 2005 / 2006                                             | E3                   |
| 13  | `q2` / `q3` blank text instead of `\N`                                                | `qualifying`               | 22 / 46 cells                                                           | A1                   |
| 14  | No `q1` time                                                                          | `qualifying`               | 156 rows                                                                | E2, E3               |
| 15  | Same team, different ID in qualifying and results                                     | `qualifying` vs. `results` | 10 rows (Marussia / Manor Marussia, 2015)                               | E6                   |
| 16  | Sprint result set the Sunday grid (so grid ≠ qualifying)                              | 2021-2022 sprint weekends  | 6 races                                                                 | E5                   |
| 17  | Standings include the race itself                                                     | standings tables           | 99.4% of rows                                                           | F1                   |
| 18  | Round 1: no earlier race in the season                                                | standings                  | 1,738 result rows                                                       | F2                   |
| 19  | Driver's first race of a season is not round 1                                        | standings                  | 1,490 driver-seasons                                                    | F3                   |
| 20  | Standings rows for drivers who did not race that weekend                              | `driver_standings`         | 8,664 rows                                                              | F1                   |
| 21  | No team standings before 1958                                                         | `constructor_standings`    | 64 races                                                                | F4                   |
| 22  | Double points race                                                                    | `results`, standings       | Abu Dhabi 2014 (50 for a win)                                           | F5                   |
| 23  | Special standings labels `D` / `E`                                                    | standings `positionText`   | 1 / 17 rows                                                             | F6                   |
| 24  | Sprint points inside the standings                                                    | standings, 2021+           | 18 sprint races                                                         | F5                   |
| 25  | Team renamed between seasons (new ID)                                                 | `constructors`             | Many teams                                                              | G3, J3               |
| 26  | Driver's first ever race (no history)                                                 | all form features          | 861 debuts                                                              | G5                   |
| 27  | Indianapolis 500 counted as an F1 race                                                | `races`                    | 11 races, 405 rows                                                      | C3, I5               |
| 28  | Same country under two labels                                                         | `circuits.country`         | `USA` / `United States`                                                 | I3                   |
| 29  | Dual, historical or misspelled nationalities                                          | `drivers.nationality`      | `American-Italian`, `East German`, `'Argentinian '`                     | I1, I2, A5           |
| 30  | Circuits used very few times                                                          | `races`                    | 24 circuits used 3 times or fewer                                       | H3                   |
| 31  | Unclear retirement reasons                                                            | `status`                   | `Retired`, `Technical`, `Damage`, `Collision damage`...                 | J1                   |
| 32  | Pit-stop duration written in minutes                                                  | `pit_stops.duration`       | e.g. `16:44.718`                                                        | A3                   |
| 33  | Lookup values never used                                                              | `constructors`, `status`   | Eagle (team 88); "+49 Laps", "+38 Laps"                                 | none (note in audit) |
