# F1 Podium Project: Data Overview (no decisions taken)

## Context
Milestone 1 predicts, per (raceId, driverId), whether `positionOrder <= 3`, using only information known after qualifying and before the race. The user wants a full understanding of the 14 CSVs and how they connect before any design choices. This file records what the data shows (all numbers from read-only pandas checks) and lists the open decisions, deliberately undecided.

## 1. Table map (rows x key facts)
| Table | Rows | PK | Role for us |
|---|---|---|---|
| races | 1,125 (1950-2024, 7-24/season) | raceId | Spine: year, round, circuitId, date. `time` only from 2005. fp/quali/sprint dates only from 2021 (mostly `\N`). |
| results | 26,759 | resultId (real grain = raceId+driverId, NOT unique) | Target source (positionOrder), grid, status, post-race fields. |
| qualifying | 10,494 (494 races) | qualifyId; (raceId,driverId) unique | Pre-race: position, q1/q2/q3. |
| drivers | 861 | driverId | nationality, dob (all parse). number 802 `\N`, code 757 `\N`. |
| constructors | 212 | constructorId | name, nationality. One `&amp;` entity. |
| circuits | 77 | circuitId | country, lat/lng/alt. |
| status | 139 | statusId | Reason a race ended (post-race; Q3 only). |
| driver_standings | 34,863 | driverStandingsId | Cumulative points/rank AFTER each race. |
| constructor_standings | 13,391 (1958+) | constructorStandingsId | Same, per team. |
| constructor_results | 12,625 (1958+) | constructorResultsId | Race points per team (status 'D' x17). |
| sprint_results | 360 (18 races, 2021-24) | resultId | Pre-race sprint outcome. |
| pit_stops | 11,371 (2011+) | raceId+driverId+stop | Post-race. Never a feature. |
| lap_times | 589,081 (1996+) | raceId+driverId+lap | Post-race. Never a feature. |
| seasons | 75 | year | Lookup only. |

Join graph: results -> races (raceId) -> circuits (circuitId) and seasons (year); results -> drivers, constructors, status; qualifying -> results on (raceId, driverId); standings -> results on (raceId, driverId) / (raceId, constructorId); sprint_results -> results on (raceId, driverId).

## 2. Integrity: verified
- All 14 primary keys unique and non-null. 23 foreign-key relations checked: 0 orphans. Every race has results. No full-row duplicates anywhere.

## 3. Findings that shape the project
**Grain / duplicates**
- 85 duplicate (raceId, driverId) groups = 176 rows, years 1950-1964 plus one 1978 case (Ertl, two DNQ rows, not a shared drive). 79 groups of 2 rows, 6 of 3.
- Pattern: original row (low resultId, driver's starting car, usually `R`) plus an appended row (higher resultId, car taken over, different grid, often the real classified finish). 69 groups same constructor, 16 different.
- The brief's example rule "non-zero grid" does not separate them: only 3 of 85 groups have grid 0 on both rows; the rest are non-zero on both.
- Podium label differs between the two rows in 21 of 85 groups. Rule effect on total podium rows: best-positionOrder 3,395; first-resultId 3,379.
- Second shared-drive form (different drivers, same positionOrder): 228 rows in 1950-1964, so 18 races have 4/5/7 podium rows. No (raceId, driverId) rule removes these (3 of the 18 are Indy 500).
- `positionOrder` is not always 1..n: 46 races (all pre-1965).
- `position` differs from `positionOrder` in 13 rows (1983 Brazilian GP, disqualifications). This confirms positionOrder is the post-disqualification classification.

**Target / base rate**
- Overall podium rate 12.7%. By era: 9.5% (1989-94) to 15.0% (2022-24). Mean rows/race: ~31.6 in 1989-94, 20.0 in 2022-24.
- Podium rows are almost all `Finished` (3,231) or `+1 Lap` (128).
- Podium rate by grid slot (grid 1/2/3): 1950-80: .50/.47/.39; 2001-13: .77/.59/.46; 2014-21: .81/.71/.59; 2022-24: .79/.72/.44. Pole is strongest and strengthens over time, which supports era sensitivity.

**`grid = 0` is overloaded**
- 1,638 rows with grid 0; 95.6% have laps = 0 (DNQ 1,013, DNPQ 331, Withdrew 164), mostly 1957-1994.
- True pit-lane starts exist only 2015-2024 (72 rows with laps > 0, 0 podiums). The brief's "0 = pit-lane start" holds only for the modern era.
- Non-start rows (DNQ/DNPQ/Withdrew/107%): 1,613 rows (about 6%), 0 podiums, 1,300+ of them in 1957-1994. Known before the race.

**Qualifying coverage (drift)**
- 1950-1993: none. 1994: 94%. 1995: 100%. 1996-2002: 6-59% (1999-2002 under 25%). 2003-2024: ~100%.
- q1 from 1994, q2 from 2005, q3 from 2006.
- Second missing-value form: 22 q2 and 46 q3 cells are empty strings (not `\N`) in recent seasons.
- 59 result rows in covered races have no qualifying row (31 with grid > 0).
- Qualifying position equals grid in only 76.7% of covered rows. Grid is higher (worse) than qualifying position in 5.1% (penalty/drop). Grid is lower (better) in 18.2%. The remainder match. 87 rows have grid 0 but a qualifying row. This is why Q1 must keep both columns.

**Standings (leakage trap)**
- Standings at race R include R's own points (delta matches race points in 99.4% of rows; round-1 standing = race points in 100%). They must be shifted back one race (previous round, or last race of the prior season for round 1) to be leakage-safe. The 2022+ deviation (0.95) comes from sprint points being included.
- 469 result rows have no driver-standings row (mostly 1990s). 8,664 standings rows have no result row that race (drivers carried over).
- constructor_standings and constructor_results start in 1958 (64 early races have none).

**Sprints**
- 18 races: 2021 (3), 2022 (3), 2023 (6), 2024 (6). In 2021-22 sprint finish vs main grid matches 43% / 60%; in 2023-24 only 12% / 17% (consistent with the format change).

**Dirty values / typing**
- `\N` is the sentinel: results.position (10,953), time/milliseconds (19,079), fastestLap* (~18.5k), rank (18,249), races date/time columns, drivers.number/code, qualifying q1/q2/q3, constructor_results.status, sprint fields.
- Lap/duration strings: `m:ss.mmm`, `h:mm:ss.mmm`, `+x.xxx` gaps. Dates parse cleanly. UTF-8 is valid (accents are fine).
- Label noise: circuits.country has both `USA` and `United States` (2 Las Vegas races); drivers.nationality has trailing-space `'Argentinian '`, dual `American-Italian`, `Argentine-Italian`, and `Monegasque`/`Dutch`/`Swiss`/`East German`/`Rhodesian` that don't match country names; `Lotus-Pratt &amp; Whitney`.

**Question-specific groundwork**
- Q1: needs races -> circuits plus qualifying.position vs results.grid; era split at 2014; coverage limits Q1 mostly to 1994+ for qualifying position (grid covers all years).
- Q2: 11 Indy 500 races (1950-1960) at one US circuit. Needs a nationality -> country map (British->UK, American->USA, etc.).
- Q3: 2014-2021 vs 2022-2024. 62 distinct status values appear in 2014-24. Ambiguous ones (`Retired`, `Mechanical`, `Technical`, `Damage`, `Debris`, `Puncture`, `Wheel`, `Collision damage`, `Withdrew`) need an explicit documented mapping. Team lineages split across ids (Force India->Racing Point->Aston Martin; Toro Rosso->AlphaTauri->RB; Sauber->Alfa Romeo; Lotus F1->Renault->Alpine; Marussia->Manor).

## 4. Open decisions: all DEFERRED by the user (not decided)
1. Shared-drive dedup rule (and handling of the same-positionOrder car shares).
2. Modeling window (full history vs 2003+, qualifying handling).
3. Non-start rows and Indianapolis 500: keep or drop.
4. Sprint features: use or exclude.
5. Also pending: nationality->country map, status->mechanical map, constructor lineage, grid=0 handling, primary/secondary metric, the "five metrics" ambiguity in the brief.

## 5. Proposed next step (only after the user is ready)
Nothing is implemented now. When the user wants to proceed, begin `ACL2.ipynb` (currently one empty cell) with a read-only Section 1: loader that maps `\N` to NaN, per-table audit and PK/FK checks, and before-cleaning EDA plots (coverage by year, podium rate by grid and era, duplicate patterns). Each decision above becomes its own labelled cell with a before/after comparison, so trial-and-error is visible, as the brief requires.

Environment note: system Python has only pandas 3.0.0 and numpy. matplotlib, scikit-learn, shap, lime, and a deep-learning library (torch/keras) are not installed anywhere, and the project .venv has no packages. They must be installed before plotting and modeling (the user has not been asked yet).

## Verification
Re-run the scratchpad scripts (schema.py, keys.py, grain.py, dedup.py, quali.py, standings.py) to reproduce any number above. They are read-only.
