# F1 Podium Project: Decisions and Edge Cases

Working list of every decision the project needs and every edge case found in the data. Kept outside the notebook; the notebook discovers these facts with code.

## Plan: the steps, in order

Notebook: `F1_podium_prediction.ipynb`. Deadline: **18 October 2026, 11:59 PM**. Update the **Status** column as we go.

| # | Step | What happens | Decisions settled here | Status |
|---|---|---|---|---|
| 1 | Load the data and first look | Load every CSV as plain text; look at the first rows of each table; describe the tables and how they connect | – | Done |
| 2 | Missing values, table by table | Count blank cells and placeholders per column; for each table say whether the gaps matter and which columns we keep | A1, A4, D1, E3, E4 (partly) | Done |
| 3 | Formats and data types | Find columns written in more than one format (e.g. race times, pit-stop durations) and text that should be numbers or dates | A2, A3, F6 | Done |
| 4 | Keys and links | Check primary keys (unique, never empty) and foreign keys (every link points to a real row) | – | Done |
| 5 | Duplicates | Fully identical rows, repeated IDs, and the same driver twice in one race (shared cars); choose and explain a rule | B1-B4 (all decided) | Done (checks, scenarios, B1 rule, B3 and B4 are in the notebook; `results_one_row` is the result) |
| 6 | Exploring the data (EDA) | Podium rate, grid vs. podium, qualifying coverage per season, `grid = 0`, number of cars per race, with plots | – (gives the evidence for step 7) | Done (6 analyses and a summary table in the notebook) |
| 7 | Decisions and cleaning | Drop unused columns, fix duplicates, choose rows and seasons, fix labels; show before/after counts and repeat key plots | C, D2, D3, E1, E2, E4-E6, F1-F5, A5 (and apply A1-A4) | To do |
| 8 | Feature engineering | Build features using only information known before the race: grid, qualifying, standings before the race, recent form from **past races** (sort by date, group by driver / team, shift by one race); show evidence for each feature | G, L1-L3 | To do |
| 9 | The three data-engineering questions | Q1 front row → podium by circuit, Q2 home advantage, Q3 mechanical failures by team; each with joins, a plot and an answer | H, I, J | To do (after step 7) |
| 10 | Split, models, experiments, explanations, prediction function, report | Season split, baseline + second model + small neural network, ablation and preprocessing-order experiments, SHAP / LIME, prediction function, PDF report | K, L4-L10, M | To do |

**Rule for past-race features (step 8):** for the race being predicted, only use what is known before it starts: anything from **earlier** races (positions, points, status, standings after the previous race) plus this race's grid and qualifying. Never use this race's own result, points, time or status (that is leakage).

## Decisions to Take

Every choice the project needs, from the biggest to the smallest. When a decision is made, the **Decided** column gives the choice and where it is written in the notebook (section → table). Everything else is still **open**.

**Decided so far:** A1, A2, A3, A4, B1, B2, B3, B4, C1, C2, C3, C6, C7, D1, E1, E3, E4 (partly), F6.

### A. Loading and data types
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| A1 | What counts as an empty value | Only `\N` · also blank text | `q2` / `q3` have 22 / 46 blank cells besides `\N` | **Both `\N` and blank text are missing.** (Missing values → `qualifying`) |
| A2 | How to turn lap times into numbers | Seconds · milliseconds | `q1`-`q3` are text like `1:27.452` | **Seconds**, e.g. `1:26.572` → 86.572. All `q1`-`q3` use one format (min:sec), so one rule works. (Formats → intro, `qualifying`) |
| A3 | What to do with mixed-format times | Convert · drop the column | `pit_stops.duration` is `26.898` or `16:44.718`; `results.time` is the winner's time or a gap (`+5.478`) | **Not converted.** All mixed columns (`results.time`, `sprint_results.time`, `pit_stops.duration`, every `positionText`) are post-race or replaced by another column, so they are not used. (Formats → `results`, `sprint_results`, standings, `pit_stops`) |
| A4 | Which columns to drop as useless | e.g. `url`, practice dates, `code` | Practice and qualifying dates are empty before 2021 | **Keep only:** `races`: `raceId`, `year`, `round`, `circuitId`, `name`, `date` · `results`: `raceId`, `driverId`, `constructorId`, `grid`, `positionOrder`, `points`, `statusId` · `qualifying`: `raceId`, `driverId`, `position`, `q1`-`q3`. **Drop** e.g. session dates/times, `drivers.number` / `code`, `constructor_results.status`, race-time and fastest-lap columns. (Missing values → `drivers`, `races`, `results`, `qualifying`, `constructor_results`) |
| A5 | How to clean text labels | Strip spaces · fix `&amp;` | `'Argentinian '` (trailing space), `Lotus-Pratt &amp; Whitney` | open |

### B. One row per driver per race (duplicates)
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| B1 | Which row to keep when a driver has 2-3 rows in one race | Best finishing position · the car he started in (first `resultId`) · most laps · drop the driver | 85 cases (176 rows). The brief's "non-zero grid" rule fails: in 82 of 85 cases both rows have a grid position | **Keep the row of the car the driver started in: the row with the lowest `resultId` of each pair.** Reasoning below. **Applied** in the notebook (Duplicates → "Applying the rule"): 26,759 → 26,668 rows, 91 removed, new table `results_one_row`. |
| B2 | Which grid and team to keep for that driver | Take them from the kept row · from the car he started in | If the kept row is the car he took over, its grid is that car's, not his own | **Grid and team come from the same kept row**, so they describe the car he started in. (Same row as B1; nothing is mixed from the other row.) |
| B3 | What to do when two drivers share one car's result | Both get the podium · only one · drop | 18 races have 4, 5 or 7 podium rows because of shared cars | **Keep both drivers.** Every driver who shares a finishing place keeps his own row and the same label. After B1 this affects 38 shared places (77 rows), of which only 4 are on the podium (8 rows, in 1951 and 1955). Reasoning below. |
| B4 | Accept races where `positionOrder` is not 1, 2, 3, ... | Accept · renumber | 46 early races (all before 1965) | **Accept the finishing places as they are, no renumbering.** Renumbering would change 371 rows in 28 races and flip 4 podium labels (the shared podium places), contradicting B3. Only places 1-3 are used by the target, and no race is missing place 1, 2 or 3. (Duplicates → B4 cells) |

#### Why B1 and B2: keep the car the driver started in (quantitative reasoning)

Numbers are from the repeated pairs in `results`: 85 driver-race pairs (79 with 2 rows, 6 with 3 rows), 176 rows, 91 of them "later rows" (a pair's rows other than the first). They fall in 1950-1964, plus one pair in 1978. "First row" = lowest `resultId` of the pair.

1. **The rows of a pair are different cars.** In all 85 pairs the car numbers differ between the rows (0 pairs share a number). Inside one race a car number identifies a car: 26,452 of 26,592 (race, number) combinations belong to a single driver.
2. **The later row is usually another driver's car result.** 84 of the 91 later rows (92%) have the same grid and finishing place as another driver's row in the same race. Only 29 of the 85 first rows (34%) do, and that figure is an upper bound: it also counts a first row whose car was later taken over by someone else (the first row is still the driver's own car).
3. **Effect of each rule on the 85 kept rows** (rows that carry another car's grid and place):

| Rule | Kept rows carrying another car's grid and place | Podium rows among the 85 |
|---|---|---|
| **First row (car he started in)** | **29 (34%)** | 6 |
| Best finishing place | 80 (94%) | 22 |
| Most laps | 80 (94%) | 22 |
| Last row | 78 (92%) | 17 |

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
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| C1 | Keep drivers who never started? | A keep all · **B drop `grid = 0`** · C drop `grid = 0` before 2015 only | 1,635 rows have `grid = 0` (6.1%), none is a podium. The grid slot is known before the race | **B: remove every row with `grid = 0`** (26,668 → 25,033 rows; all 3,379 podium rows stay). The filter uses only `grid`, never `laps` or `status` of the race. Reasoning below. |
| C2 | How to define "started the race" | `grid > 0` · `laps > 0` · either · by status | 966 rows have a grid slot but 0 laps (lap-1 crashes); 84 "Withdrew" rows still have a grid slot | **A: "started" means a grid slot (`grid > 0`) and nothing else.** Rows with a grid slot and 0 laps (966) stay, and so do rows whose status says Withdrew / Did not qualify / Excluded but have a grid slot (98). `laps` and `status` of the race are post-race and are not used to select rows. Reasoning below. |
| C3 | Keep the Indianapolis 500? | Keep · drop | 11 races (1950-1960); 381 rows after B1 (405 raw); 103 of its 107 drivers never raced elsewhere in F1 (corrected from 104: only Ascari, Ward, Ruby and Ruttman did) | **Drop the Indianapolis 500** (381 rows, 11 races, 35 podium rows: 3,379 → 3,344). Reasoning below; evidence code in the notebook ("Cleaning: which rows stay" → C3). |
| C4 | Which seasons to model | All (1950+) · 1994+ · 2003+ · 2006+ | Qualifying data: none before 1994, patchy until 2002, complete from 2003 | open |
| C5 | Use the same row filters for Q1-Q3 as for the model? | Same · decide per question | Q1 can use all years for grid; Q3 only needs 2014-2024 | open |
| C6 | Keep disqualified / excluded drivers? | Keep · drop | 155 rows in the raw table by status (147 Disqualified, 8 Excluded); 146 rows flagged in the table after B1, C1 and C3; they raced but lost their result | **Keep them.** Their label is the official classification (not a podium). Nothing is removed (24,652 rows, 3,344 podium rows). Reasoning below; evidence code in the notebook ("Cleaning: which rows stay" → C6). |
| C7 | Use sprint results as a feature? | Use (sprint finish, sprint points) · don't use | Pre-race information (1 day before the race in 18 of 18), but only 18 races (341 table rows, 1.4%) have a sprint and none is in the years up to 2019 | **Do not use.** The 341 main-race rows of sprint weekends stay (54 podium rows); only `sprint_results` is left out. Reasoning below; evidence code in the notebook ("Cleaning: which rows stay" → C7). |


#### Why C1 = B and E1: remove every row with `grid = 0` (quantitative reasoning)

Counts are from `results_one_row` (26,668 rows, after B1).

**What `grid = 0` contains**

| Group | Rows | Podiums | Notes |
|---|---|---|---|
| Never ran (0 laps) | 1,563 | 0 | 1,505 of them (96%) have status Did not qualify (1,012), Did not prequalify (330) or Withdrew (163); seasons 1952-2023 |
| Ran, from the pit lane | 72 | 0 | All in 2015-2024 (1 in 2015, up to 16 in 2023); finishing places 5 to 22 (median 15); qualifying position known for 71 (5 to 22, median 18) |
| **Total** | **1,635** | **0** | 6.1% of the rows |

**Reasons for removing them**

1. **The 72 pit-lane rows are too few to teach the model anything and could add noise (team's reason).** They are 0.27% of the rows. The grid is the strongest feature (EDA 2: podium rate falls steeply with the grid, correlation -0.39 to -0.52), and a `0` read as a number sits "ahead of pole position", against that relation.
2. **A separate flag column is not worth it (team's reason).** A pit-lane flag would be 1 on 72 rows and 0 podiums. The back of the grid in 2015+ (grid 15th or worse) has 12 podiums in 1,225 rows (0.98%), so about 0.7 podiums would be expected in 72 rows. Seeing 0 is what chance gives, so there is no evidence that the flag carries a signal different from "starts at the back".
3. **The other 1,563 rows are not participants.** None can finish on the podium and the grid slot says so before the race.
4. **Keeping them flatters the scores.** AUC of the grid alone: 0.890 with them and 0.881 without (train); 0.935 and 0.923 in 1990-94; 0.914 and 0.911 in the test years. The model would be credited for "predicting" drivers who were not in the race, and the podium rate is diluted (12.7% against 13.5%).
5. **It is a pre-race rule.** The grid is known before the race. `laps` and `status` of the same race are not, so we cannot drop rows with them (see the 966 rows below).
6. **In 2015+ the two meanings cannot be separated before the race.** Of the 79 modern `grid = 0` rows, 72 ran and 7 did not; both look the same (`grid = 0`), so a rule "keep modern `grid = 0`" would keep 7 non-participants.
7. **One rule, easy to defend.** Option C needs a year boundary (2015) that we would have to justify, for 72 rows with no podium.

**Options not chosen**

| Option | Rows | Why not |
|---|---|---|
| A keep all | 26,668 | Reasons 3 and 4: 6.1% of rows are non-participants and the scores are flattered |
| C drop `grid = 0` before 2015 only | 25,112 | Reasons 2 and 6: keeps 79 rows (7 non-participants) that carry no usable signal, and needs a year rule |

**Costs and limitations (to state in the report)**
- The model never sees a pit-lane start (72 rows, 0.27% of the data, 0 podiums).
- The 966 rows with a grid slot and 0 laps (lap-1 crashes) **stay**: they are only known after the race starts. They carry 0 podiums but are legitimate prediction rows.
- If someone passes `grid = 0` to the prediction function, it is replaced by the last slot of that race (an assumption, not learned from data).
- The filter removes no podium row: 3,379 before and after.

#### Why C2 = A: keep every row that has a grid slot, also with 0 laps

Counts are after C1 (25,033 rows with `grid > 0`).

| Group (all have a grid slot) | Rows | Podiums | Top statuses |
|---|---|---|---|
| 0 laps | 966 (3.9%) | 0 | Collision 353, Accident 233, Withdrew 61, Engine 47, Spun off 38, Gearbox 34 |
| Status Withdrew / Did not qualify / Excluded | 98 (73 of them also in the 0-lap group; 25 have laps) | 0 | Withdrew 84, Did not qualify 12, Excluded 2 |

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

| Measure | Indianapolis 500 | Other races, 1950-1960 |
|---|---|---|
| Rows | 381 (11 races) | 1,763 |
| Rows per race | 34.6 | 21.2 |
| Podium rate (rows with a grid slot) | 9.2% | 14.9% |

1. **95% of its rows have no history.** 103 of its 107 drivers never appear in any other race; they hold 362 of its 381 rows and 32 of its 35 podium rows. Past-race features (form, team form, standings) are empty for them by construction, and they cannot be compared with regular drivers. Only Ascari, Ward, Ruby and Ruttman raced elsewhere.
2. **Its structure is different:** 34.6 rows per race against 21.2, a lower podium rate, and 21 of the 85 repeated driver-race pairs (25%) are in this race.
3. **It would distort Question 2 (home advantage)**, as the introduction warns.
4. **The cost is limited to 1950-1960:** 35 podium rows (3,379 → 3,344, 381 rows). It changes nothing for any training window that starts later.
5. **The introduction names exclusion as a defensible choice** (allowed source); the data above is our own evidence for it.

**Cost:** 35 podium rows, all in 1950-1960. Q2 loses the American drivers' Indianapolis races.

#### Why C6: keep the disqualified and excluded rows

Counts are for the table after B1, C1 and C3 (24,652 rows).

| Measure | Value |
|---|---|
| Rows flagged (status `Disqualified`/`Excluded`, or `positionText` D/E) | **146** (0.59%): 142 by both markers, 4 by the letter only, 0 by status only |
| Raw table, for reference | status: 147 Disqualified + 8 Excluded = 155; `positionText`: 151 D + 9 E = 160 |
| Podium rows among the flagged | **0** |
| Completed at least 90% of the laps of the race | 76 (13 started in the top 3, 10 of them on the front row) |
| Of those 76, ranked below all unflagged full-distance finishers | 76 of 76 |
| By decade | 1950s: 5, 1960s: 9, 1970s: 25, 1980s: 51, 1990s: 20, 2000s: 22, 2010s: 9, 2020s: 5 (110 before 2000, 36 from 2000) |
| Races with a flagged row | 109 of 1,114 (327 of the 3,344 podium rows are in those races) |
| Podium rate keeping / dropping | 13.56% / 13.65% (3,344 podium rows either way) |

1. **A disqualification is known only after the race.** Dropping the rows would select rows with the result of the race, which is the principle used in C1 and C2.
2. **It is consistent with D1.** The target is the final classification (`positionOrder`). In the 1983 Brazilian GP, `position` and `positionOrder` differ in 13 rows and one driver gets a podium label he would not have had; those promoted drivers are podiums *because* of the disqualification. Removing the disqualified row but keeping the promoted ones would be inconsistent.
3. **`positionOrder` already handles them.** All 76 full-distance flagged rows are ranked below every unflagged full-distance finisher, so a disqualified driver is a clean negative.
4. **Dropping would flatter the scores.** The 13 cars that started in the top 3 and ran the full distance are the hard cases a real prediction faces.
5. **The size is negligible:** 0.59% of the rows and no podium row.
6. **No definition is needed.** Status and `positionText` differ on 4 rows; keeping all rows avoids choosing between them.

**Cost / limitation (state in the report):** about 13 drivers who looked like podium finishers on the road (top-3 grid, full distance) carry the label "not a podium". This label noise is not visible in the data.

#### Why C7: do not use the sprint results as features

Counts are for the table after B1, C1 and C3 (24,652 rows).

| Measure | Value |
|---|---|
| Sprint races | 18 (2021: 3, 2022: 3, 2023: 6, 2024: 6); `sprint_date` is 1 day before the race date in all 18 |
| Table rows in sprint weekends | **341** (1.4%), 54 podium rows; up to 2019: **0**, 2020-2021: 56, 2022-2024: 285 |
| Rows with a sprint result in a training window | up to 2019: 0; up to 2021: 56 (0.24%); up to 2022: 113 (0.48%) |
| Podium rate: sprint weekends / other races of 2021-2024 | 15.8% / 15.4% |
| Corr. with podium (grid on the same rows: -0.45) | sprint place -0.47, sprint points 0.53, sprint grid -0.42, team's best sprint place -0.48, team's sprint points 0.51, places gained 0.06, completed 0.01 |
| Same, after removing what the grid explains | -0.25, 0.38, -0.20, -0.25, 0.34, 0.02, -0.02 |
| Grid equals sprint place | 2021-2022: 62 of 113 rows (the sprint result set the Sunday grid); 2023-2024: 35 of 228 |

1. **It cannot be learned.** With the training years of the introduction (up to 2019, K1 still open) the column would be constant; training up to 2022 gives only 113 rows (0.48%).
2. **It would be empty for 98.6% of the rows.** Every fill is an assumption: 0 reads "won the sprint", a large number "finished last", a mean "midfield"; only the row's own grid position is neutral, and then the column adds nothing for 98.6% of rows.
3. **The evidence is thin:** 341 rows in 18 races, and in 2021-2022 part of the signal is the grid itself.
4. **It is not rejected for leakage:** the sprint is the day before the race, so it is pre-race information. It is left out because it cannot be trained and tested honestly. State this as a limitation in the report.
5. **No special case** for 1 row in 70; every model gets the same features.

**Cost:** a possible extra signal in the sprint weekends of 2021-2024 (the sprint place keeps a correlation of -0.25 with the podium after the grid is removed). It can be tested later as an experiment on 2021 and later only.

**Not decided here:** whether sprint failures count in Question 3 (J5).

### D. Target
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| D1 | Confirm the target | `positionOrder <= 3` | `positionOrder` already includes post-race disqualifications (e.g. 1983 Brazilian GP) | **`positionOrder` 1, 2 or 3 = podium.** It is never missing, unlike `position`. (Missing values → `results`) |
| D2 | How to handle podiums being rare | Class weights · resampling · nothing | About 13% podiums overall (9.5% in 1989-94, 15% in 2022-24) | open |
| D3 | Force exactly 3 podiums per race in predictions? | Yes (top 3 per race) · no (fixed threshold) | A plain threshold can predict 0 or 6 podiums in one race | open |

### E. Grid and qualifying features
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| E1 | What `grid = 0` means as a feature | Last place · empty · separate pit-lane flag | Before 1995 it means "never started"; from 2015 it means a pit-lane start (72 rows) | **No `grid = 0` rows in the table (follows from C1 = B), no pit-lane flag.** The prediction function treats a given `grid` of 0 as "starts from the pit lane" and uses the last slot of the race; the report states the model never saw this case. Reasoning below. |
| E2 | What to do when a race has no qualifying data | Fill in · use grid instead · drop those seasons · add a "missing" flag | All races before 1994, most races 1996-2002 | open |
| E3 | How to use `q2` / `q3` when empty | "Knocked out" flag · use best available time | Empty means "knocked out" from 2005/2006, but "session did not exist" before that | **Not filled in.** The three times become one number: the driver's best qualifying time (from whichever of `q1`-`q3` exists). (Missing values → `qualifying`) |
| E4 | How to compare lap times between races | Raw seconds · gap to pole (seconds or %) | Every track has a different lap length, so raw times are not comparable | **Partly decided:** compare the best time with the fastest driver in that race (gap to pole). Seconds or % still **open**. (Missing values → `qualifying`) |
| E5 | Use qualifying position, grid, or both? | One · both · their difference | They match in only 77% of rows (penalties) | open |
| E6 | Which team ID to trust when qualifying and results disagree | Results · qualifying | 10 rows in 2015: "Marussia" in qualifying vs. "Manor Marussia" in results | open |

### F. Standings before the race
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| F1 | How to find "the previous race" | Same season, `round - 1` · by date | `year` + `round` is unique, so this is safe | open |
| F2 | What to use for round 1 | 0 · last season's final standings · empty | Round 1 has no earlier race in the season (1,738 result rows) | open |
| F3 | What to use when a driver has no earlier row this season | 0 · empty | 1,490 of 3,211 driver-seasons start after round 1 (new or replacement drivers) | open |
| F4 | Team standings before 1958 | Empty · drop those seasons | The constructors' championship started in 1958 (64 races without it) | open |
| F5 | How to compare points across eras | Raw points · rank · share of the leader's points | A win was worth 8-10 points before 2010 and 25 after; Abu Dhabi 2014 gave double points (50) | open |
| F6 | How to treat special standings labels | Ignore · treat as last | `positionText` has `D` (1 driver row) and `E` (17 team rows): disqualified / excluded from the championship | **Ignore `positionText`; use `position`**, which is always a number. (Formats → `driver_standings`, `constructor_standings`) |

### G. Recent-form features (from past races only)
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| G1 | How many past races to look at | Last N races · season so far · whole career | Short windows react fast but are noisy | open |
| G2 | Driver form, team form, or both | — | The car usually matters more than the driver | open |
| G3 | Follow teams through renames? | Use `constructorId` (history resets) · build a team-lineage map | Toleman → Benetton → Renault → Lotus → Alpine; Toro Rosso → AlphaTauri → RB | open |
| G4 | Which team's form for a driver who changed team mid-season | Current team · previous team | Common in the 1960s (17% of drivers), rare today (2%) | open |
| G5 | What to use for a driver's first race (no history) | 0 · empty · average | Every driver has a debut (861) | open |
| G6 | Reset form at the start of each season? | Reset · carry over | Cars change a lot between seasons | open |
| G7 | Which past results to measure | Podium rate · average finish · points · DNF rate | Each tells a different story | open |
| G8 | Do past non-starts count in form? | Count · skip | A "did not qualify" is not a race result | open |
| G9 | Add circuit history (driver at this track)? | Yes · no | Few races per driver per circuit, so it is noisy | open |
| G10 | Add the year or era as a feature? | Yes · no | Podium patterns change by era | open |

### H. Question 1 (front row → podium, by circuit)
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| H1 | Front row by grid, by qualifying, or both | The question asks to compare both | Qualifying exists only from 1994 | open |
| H2 | Which years count as "before 2014" | All years · 1994-2013 · 2003-2013 | A fair comparison needs similar periods | open |
| H3 | Minimum races for a circuit to be ranked | e.g. at least 5 races per period | 24 circuits were used 3 times or fewer, 11 only once | open |

### I. Question 2 (home advantage)
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| I1 | How to match nationality to country | Write a mapping table | "British" → "UK", "American" → "USA", "Monegasque" → "Monaco", "Dutch" → "Netherlands" | open |
| I2 | Dual and historical nationalities | Pick one country · count both · drop | "American-Italian", "Argentine-Italian", "East German", "Rhodesian" | open |
| I3 | Merge `USA` and `United States` | Yes | Same country under two labels | open |
| I4 | How to control for starting position | Compare within grid groups (e.g. 1-3, 4-6...) · logistic regression with grid | The brief requires this control | open |
| I5 | Drivers from countries that never hosted a race | Exclude · keep as "never home" | e.g. Finnish, New Zealander, Danish, Irish, Colombian drivers | open |

### J. Question 3 (mechanical failures by team)
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| J1 | Which statuses count as "mechanical" | Write a mapping for all statuses that occur | 62 different statuses appear in 2014-2024; some are unclear: `Retired`, `Technical`, `Damage`, `Collision damage`, `Puncture`, `Out of fuel` | open |
| J2 | What to divide by | Race starts only · all entries | Drivers who never started cannot fail | open |
| J3 | Per `constructorId` or per team lineage | — | Teams were renamed between the two eras | open |
| J4 | Minimum starts for a team to be shown | e.g. 20 starts | Teams with very few starts give extreme rates | open |
| J5 | Count sprint failures? | Yes · no | Sprints exist only from 2021 | open |

### K. Split and evaluation
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| K1 | Confirm the season split | Train ≤ 2019 · validation 2020-2021 · test ≥ 2022 | Given in the intro PDF | open |
| K2 | Main and second metric | e.g. PR-AUC main, ROC-AUC second | The brief asks us to justify the choice; podiums are rare | open |
| K3 | How to choose the decision threshold for F1 | Best F1 on validation · top 3 per race | Must use validation, never test | open |
| K4 | The brief's "all five metrics" | Add precision, recall, accuracy · ask | Only three metrics are listed in the brief | open |
| K5 | Retrain on train + validation before testing? | Yes · no | More data vs. a cleaner comparison | open |
| K6 | Treat 2020 as a normal season? | Yes · note it | COVID season: only 17 races | open |

### L. Preprocessing and models
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| L1 | How to fill missing feature values | Median · constant · add "missing" flag | Learned on train only, to avoid leakage | open |
| L2 | Scale numeric features? | Standard · min-max · none | Needed for logistic regression and the neural network | open |
| L3 | How to encode IDs (driver, team, circuit) | Drop · one-hot · target encoding | Target encoding can leak the answer | open |
| L4 | Which two preprocessing orders to compare | e.g. fill-then-scale vs. scale-then-fill; filter before vs. after building features | The brief requires at least two | open |
| L5 | Baseline model | e.g. logistic regression | Required reference point | open |
| L6 | Second statistical model | Random forest · gradient boosting | At least two statistical models required | open |
| L7 | Neural network library and size | PyTorch · Keras · scikit-learn MLP; 1-2 hidden layers | Not installed yet | open |
| L8 | How to tune settings | Grid search · random search · manual | Validation set only | open |
| L9 | Feature groups for the ablation | e.g. grid · qualifying · standings · form · driver/circuit info | Required experiment | open |
| L10 | Random seed | Fix one seed | So results can be repeated | open |

### M. Explanations and the prediction function
| # | Decision | Options | Why it matters | Decided |
|---|---|---|---|---|
| M1 | Which model to explain | The best one · all | SHAP and LIME take time | open |
| M2 | Which race / driver to explain locally | A correct podium · a surprising miss | One example is required | open |
| M3 | Input format of the prediction function | Dictionary · one-row table | Must work with missing values | open |
| M4 | Which incomplete record to demonstrate | e.g. a row with no qualifying data | The brief asks for a complete and a partial record | open |

---

## Edge Cases to Handle

Concrete situations in our data that the code must deal with. Each one links to the decision above that settles it.

| # | Edge case | Where | Count | Decision |
|---|---|---|---|---|
| 1 | Same driver appears 2 or 3 times in one race (shared cars) | `results` | 85 cases, 176 rows (1950-1964) | B1, B2 |
| 2 | One driver listed twice only because he failed to qualify with two teams (Ertl, 1978) | `results` | 1 case | B1 |
| 3 | A driver holds two podium places in one race (Farina and Trintignant, 1955 Argentina) | `results` | 2 cases | B1, B3 |
| 4 | Two drivers credited with the same finishing place (shared car) | `results` | 228 rows; 18 races with 4-7 podium rows | B3 |
| 5 | Half or split points from shared cars | `results.points` | 42 rows with fractional points | F5, G7 |
| 6 | `grid = 0` meaning "never started" | `results` | Most of 1,638 rows, mainly 1957-1994 | C1, E1 |
| 7 | `grid = 0` meaning a pit-lane start | `results` | 72 rows, 2015-2024 | E1 |
| 8 | Grid slot but 0 laps (out on lap 1) | `results` | 966 rows | C2 |
| 9 | "Withdrew" but has a grid slot or laps | `results` | 84 with grid, 23 with laps | C2 |
| 10 | Official `position` differs from `positionOrder` after disqualifications | `results` | 13 rows (1983 Brazilian GP) | D1 |
| 11 | No qualifying row at all | `qualifying` | All races before 1994, most of 1996-2002, plus 59 rows in covered races | E2 |
| 12 | `q2` / `q3` empty because the session did not exist | `qualifying` | All rows before 2005 / 2006 | E3 |
| 13 | `q2` / `q3` blank text instead of `\N` | `qualifying` | 22 / 46 cells | A1 |
| 14 | No `q1` time | `qualifying` | 156 rows | E2, E3 |
| 15 | Same team, different ID in qualifying and results | `qualifying` vs. `results` | 10 rows (Marussia / Manor Marussia, 2015) | E6 |
| 16 | Sprint result set the Sunday grid (so grid ≠ qualifying) | 2021-2022 sprint weekends | 6 races | E5 |
| 17 | Standings include the race itself | standings tables | 99.4% of rows | F1 |
| 18 | Round 1: no earlier race in the season | standings | 1,738 result rows | F2 |
| 19 | Driver's first race of a season is not round 1 | standings | 1,490 driver-seasons | F3 |
| 20 | Standings rows for drivers who did not race that weekend | `driver_standings` | 8,664 rows | F1 |
| 21 | No team standings before 1958 | `constructor_standings` | 64 races | F4 |
| 22 | Double points race | `results`, standings | Abu Dhabi 2014 (50 for a win) | F5 |
| 23 | Special standings labels `D` / `E` | standings `positionText` | 1 / 17 rows | F6 |
| 24 | Sprint points inside the standings | standings, 2021+ | 18 sprint races | F5 |
| 25 | Team renamed between seasons (new ID) | `constructors` | Many teams | G3, J3 |
| 26 | Driver's first ever race (no history) | all form features | 861 debuts | G5 |
| 27 | Indianapolis 500 counted as an F1 race | `races` | 11 races, 405 rows | C3, I5 |
| 28 | Same country under two labels | `circuits.country` | `USA` / `United States` | I3 |
| 29 | Dual, historical or misspelled nationalities | `drivers.nationality` | `American-Italian`, `East German`, `'Argentinian '` | I1, I2, A5 |
| 30 | Circuits used very few times | `races` | 24 circuits used 3 times or fewer | H3 |
| 31 | Unclear retirement reasons | `status` | `Retired`, `Technical`, `Damage`, `Collision damage`... | J1 |
| 32 | Pit-stop duration written in minutes | `pit_stops.duration` | e.g. `16:44.718` | A3 |
| 33 | Lookup values never used | `constructors`, `status` | Eagle (team 88); "+49 Laps", "+38 Laps" | none (note in audit) |
