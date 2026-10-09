# Formula 1 Dataset: Table Reference (checked against our copy)

Kaggle / Ergast dataset (1950-2024). 14 relational CSV tables in `csvs/`.
Every column list and count below was **checked against our copy**. Items changed from the original reference are marked **[corrected]** or **[added]**.

**Pre-race usable?** means: can this information be used as a feature when predicting after qualifying and before the race starts? Anything that describes the current race's outcome is leakage.

---

## Overview

| Group | Tables | Role |
| --- | --- | --- |
| Lookup (who / where) | `circuits`, `drivers`, `constructors`, `seasons`, `status` | Describe entities. Small tables. Exist independently of any race |
| Calendar | `races` | One row per Grand Prix. The time backbone |
| Main facts | `results`, `qualifying`, `sprint_results` | What happened in each race session |
| Standings | `driver_standings`, `constructor_standings`, `constructor_results` | Championship points and ranks |
| Race-day detail | `lap_times`, `pit_stops` | Lap-by-lap and pit-stop events |

**Key IDs (foreign keys used to join tables):** `raceId`, `driverId`, `constructorId`, `circuitId`, `statusId`, `year`.

---

## 1. Lookup tables

### `circuits`
**Represents:** one racing track (e.g. Silverstone, Monaco). **77 rows.**
**Grain:** one row per circuit. **Primary key:** `circuitId`.

| Column | Meaning |
| --- | --- |
| `circuitId` | Unique ID of the circuit |
| `circuitRef` | Short text code (e.g. `monaco`) |
| `name` | Full circuit name |
| `location` | City or area |
| `country` | Country where the circuit is (e.g. "UK", "USA") |
| `lat`, `lng` | Coordinates |
| `alt` | Altitude in metres |
| `url` | Wikipedia link |

**Relations:** `races.circuitId` -> `circuits.circuitId`.
**For this project:** `country` is needed for Q2 (home race). It is a country name ("UK"), while `drivers.nationality` is a demonym ("British"), so you need a mapping between them. **[added]** `country` also has two labels for the same country: `USA` and `United States` (the latter for the 2 Las Vegas races), which must be merged. Q1 groups by circuit.
**Pre-race usable?** Yes, it is static information.

---

### `drivers`
**Represents:** one driver, across their whole career. **861 rows.**
**Grain:** one row per driver. **Primary key:** `driverId`.

| Column | Meaning |
| --- | --- |
| `driverId` | Unique ID of the driver |
| `driverRef` | Short text code (e.g. `hamilton`) |
| `number` | Permanent car number (modern era only: filled for just 59 of 861 drivers) |
| `code` | Three-letter code (e.g. `HAM`), empty for 757 drivers |
| `forename`, `surname` | Name |
| `dob` | Date of birth (convert to a date type) |
| `nationality` | Demonym (e.g. "British") |
| `url` | Wikipedia link |

**Relations:** referenced by `results`, `qualifying`, `sprint_results`, `driver_standings`, `lap_times`, `pit_stops` through `driverId`.
**For this project:** `nationality` is used for Q2. `dob` can give driver age at race time. **[added]** `nationality` needs cleaning: one value has a trailing space (`'Argentinian '`), and there are dual values (`American-Italian`, `Argentine-Italian`).
**Pre-race usable?** Yes (static).

---

### `constructors`
**Represents:** one team name (Ferrari, McLaren, Red Bull...). **212 rows.**
**Grain:** one row per constructor identity. **Primary key:** `constructorId`.

| Column | Meaning |
| --- | --- |
| `constructorId` | Unique ID of the team |
| `constructorRef` | Short text code |
| `name` | Team name |
| `nationality` | Team nationality |
| `url` | Wikipedia link |

**Relations:** referenced by `results`, `qualifying`, `sprint_results`, `constructor_results`, `constructor_standings` through `constructorId`.
**For this project:** a team that is renamed or sold gets a new `constructorId` (e.g. Toleman -> Benetton -> Renault), so team-history features reset at renames. Q3 groups by constructor. **[added]** This can even differ inside one weekend: in five 2015 races, `qualifying` lists the team as "Marussia" (id 206) while `results` lists "Manor Marussia" (id 209) for the same drivers.
**Pre-race usable?** Yes (the identity of the team in this race is known).

---

### `seasons`
**Represents:** one championship year (1950-2024). **75 rows.**
**Primary key:** `year`.

| Column | Meaning |
| --- | --- |
| `year` | The season |
| `url` | Wikipedia link |

**Relations:** `races.year` -> `seasons.year`.
**For this project:** almost no information on its own. Useful only as a join target.

---

### `status`
**Represents:** the list of reasons a driver's race ended. **139 rows.**
**Primary key:** `statusId`.

| Column | Meaning |
| --- | --- |
| `statusId` | Unique ID |
| `status` | Text, e.g. "Finished", "+1 Lap", "Engine", "Gearbox", "Collision", "Disqualified" |

**Relations:** `results.statusId` and `sprint_results.statusId` -> `status.statusId`.
**For this project:** Q3 needs you to group these values into mechanical failures vs. accidents, driver errors and other causes, and document the mapping. "Finished" and "+N Laps" mean the driver reached the flag, so they are not retirements. **[added]** Some statuses are ambiguous (`Retired`, `Technical`, `Damage`, `Collision damage`...) and need an explicit decision. Statuses such as "Did not qualify", "Did not prequalify" and "Withdrew" mark drivers who **never started**.
**Pre-race usable?** No. It describes the race outcome.

---

## 2. Calendar table

### `races`
**Represents:** one Grand Prix (one race event). **1,125 rows.**
**Grain:** one row per race. **Primary key:** `raceId`. **[added]** (`year`, `round`) is also unique, which makes it easy to find "the previous race in the same season".

| Column | Meaning |
| --- | --- |
| `raceId` | Unique ID of the race |
| `year` | Season |
| `round` | Race number within the season |
| `circuitId` | Where it was held |
| `name` | Grand Prix name (e.g. "British Grand Prix") |
| `date`, `time` | Race date and start time (convert `date` to a date type). `time` only exists from 2005 |
| `url` | Wikipedia link |
| `fp1_date`, `fp1_time`, `fp2_date`, `fp2_time`, `fp3_date`, `fp3_time` | Practice session schedule. **[corrected]** Empty for **every** race before 2021 |
| `quali_date`, `quali_time` | Qualifying schedule (also empty before 2021) |
| `sprint_date`, `sprint_time` | Sprint schedule (only on the 18 sprint weekends) |

**Relations:** `circuitId` -> `circuits`; `year` -> `seasons`. Referenced by almost every other table through `raceId`.
**For this project:** this is the time backbone. Result tables have no date, so you join to `races` to get the year and to order races chronologically. That ordering is what makes leakage-safe "only past races" features possible. The era splits (hybrid era 2014-2021, train <= 2019, validation 2020-2021, test >= 2022) all use `year`.
**Pre-race usable?** Yes (calendar information).

---

## 3. Main fact tables

### `results`
**Represents:** the race outcome for every driver who entered a race. **26,759 rows.** **This is the base of your modeling table.**
**Intended grain:** one row per (`raceId`, `driverId`). The raw data breaks this in early F1 because of shared drives (85 duplicated pairs, 176 rows, 1950-1964 plus one 1978 case), so you must deduplicate. **Primary key:** `resultId`.

| Column | Meaning | Pre-race usable? |
| --- | --- | --- |
| `resultId` | Unique row ID | Key only |
| `raceId` | Which race | Yes |
| `driverId` | Which driver | Yes |
| `constructorId` | Which team the driver raced for | Yes |
| `number` | Car number | Yes (low value) |
| `grid` | Starting position after penalties. **[corrected]** `0` means a pit-lane start only in the modern era (2015+, 72 rows). Before that it almost always means the driver **never started** (did not qualify / withdrew) | **Yes** |
| `position` | Official finishing position, empty if not classified | No |
| `positionText` | Position as text or a letter code (R, D, E, W, F, N) | No |
| `positionOrder` | Full ranking of every entrant, always filled | **Target only** (podium = `positionOrder <= 3`) |
| `points` | Championship points scored | No |
| `laps` | Laps completed | No |
| `time`, `milliseconds` | Finish time or gap to winner | No |
| `fastestLap` | Lap number of the driver's fastest lap | No |
| `rank` | Rank of the driver's fastest lap in the race | No |
| `fastestLapTime`, `fastestLapSpeed` | Fastest lap time and speed | No |
| `statusId` | Why the race ended | No (Q3 only) |

**Relations:** `raceId` -> `races`; `driverId` -> `drivers`; `constructorId` -> `constructors`; `statusId` -> `status`.
**For this project:** only the IDs and `grid` are safe features. Everything else describes Sunday. Past rows from this table are used to build leakage-safe form features (for example, a driver's podium rate over the previous races).

---

### `qualifying`
**Represents:** the qualifying session result for each driver. **10,494 rows (494 races).**
**Grain:** one row per (`raceId`, `driverId`), unique. **Primary key:** `qualifyId`.

| Column | Meaning |
| --- | --- |
| `qualifyId` | Unique row ID |
| `raceId`, `driverId`, `constructorId` | Race, driver, team |
| `number` | Car number |
| `position` | Qualifying position (not always equal to `grid`, because of penalties and, in 2021-2022 sprint weekends, because the sprint set the grid) |
| `q1`, `q2`, `q3` | Best lap time in each knockout part, as text like `1:27.452` (convert to seconds) |

**Relations:** `raceId` -> `races`; `driverId` -> `drivers`; `constructorId` -> `constructors`.
**For this project:** **[corrected]** coverage starts in **1994** (patchy 1996-2002, complete from 2003). Plot coverage per season. It is what lets you separate qualifying position from grid position in Q1.
**[corrected] What a missing value means depends on the year:**
- `q2` / `q3` missing **from 2005 / 2006 onward** = driver eliminated in an earlier part.
- `q2` / `q3` missing **before 2005 / 2006** = that session did not exist yet.
- `q1` missing (156 rows) = no time set.
- No qualifying row at all for a race = never recorded (all races before 1994, most races 1996-2002).
- `q2` and `q3` also contain **empty strings** (22 and 46 cells) besides `\N`. Treat both as missing.

**Pre-race usable?** **Yes.** Qualifying is known before the race.

---

### `sprint_results`
**Represents:** the result of the short Saturday sprint race, on sprint weekends only. **360 rows, 18 races (2021-2024).**
**Grain:** one row per (`raceId`, `driverId`), unique. **Primary key: [corrected] `resultId`** (not `sprintResultId` in our copy).

| Column | Meaning |
| --- | --- |
| `resultId` | Unique row ID **[corrected name]** |
| `raceId`, `driverId`, `constructorId` | Race, driver, team |
| `number` | Car number |
| `grid` | Sprint starting position |
| `position`, `positionText`, `positionOrder` | Sprint finishing position (same meaning as in `results`) |
| `points` | Sprint points (top 8 only) |
| `laps`, `time`, `milliseconds` | Sprint race data |
| `fastestLap`, `fastestLapTime` | Fastest lap in the sprint |
| `statusId` | Why the sprint ended |

**Relations:** `raceId` -> `races`; `driverId` -> `drivers`; `constructorId` -> `constructors`; `statusId` -> `status`.
**For this project:** the sprint runs before the main race, so it is technically pre-race information. Whether to use it is a judgement call you must document. It exists for only 18 of 1,125 races, so most rows would be missing.

---

## 4. Standings tables

### `driver_standings`
**Represents:** the Drivers' Championship table **after** each race. **34,863 rows.**
**Grain:** one row per driver per race, unique. **Primary key:** `driverStandingsId`.

| Column | Meaning |
| --- | --- |
| `driverStandingsId` | Unique row ID |
| `raceId`, `driverId` | Race and driver |
| `points` | Cumulative championship points after this race |
| `position` | Championship rank after this race |
| `positionText` | Rank as text |
| `wins` | Cumulative wins in the season after this race |

**Relations:** `raceId` -> `races`; `driverId` -> `drivers`.
**For this project:** the row for race X **includes the result of race X** (verified: true for 99.4% of rows), so using it directly leaks the target. You must shift to "standings before this race" by taking the previous race's row in the same season. **[corrected]** How to fill **round 1** (zero, previous season's final standings, or missing) is a **decision still to be made**, not a given. **[added]** Standings also contain rows for drivers who did **not** race that weekend (8,664 rows), and a driver who joins mid-season has no previous row.
**Pre-race usable?** Only after shifting.

---

### `constructor_standings`
**Represents:** the Constructors' Championship table after each race (exists from 1958). **13,391 rows.**
**Grain:** one row per constructor per race, unique. **Primary key:** `constructorStandingsId`.

| Column | Meaning |
| --- | --- |
| `constructorStandingsId` | Unique row ID |
| `raceId`, `constructorId` | Race and team |
| `points` | Cumulative team points after this race |
| `position` | Team rank after this race |
| `positionText` | Rank as text |
| `wins` | Cumulative team wins in the season |

**Relations:** `raceId` -> `races`; `constructorId` -> `constructors`.
**For this project:** same leakage warning as `driver_standings`. Constructor form is important because car performance is the dominant factor in most eras. Missing for the 64 races before 1958.
**Pre-race usable?** Only after shifting.

---

### `constructor_results`
**Represents:** the points a team scored in a single race. **12,625 rows (from 1958).**
**Grain:** one row per constructor per race, unique. **Primary key:** `constructorResultsId`.

| Column | Meaning |
| --- | --- |
| `constructorResultsId` | Unique row ID |
| `raceId`, `constructorId` | Race and team |
| `points` | Points scored by the team in that race |
| `status` | Rarely filled: "D" (disqualified) in 17 rows, otherwise empty |

**Relations:** `raceId` -> `races`; `constructorId` -> `constructors`.
**For this project:** post-race, so never a feature for the current race. It can be used to build past-form features from earlier races.

---

## 5. Race-day detail tables

### `lap_times`
**Represents:** the time of every lap for every driver. **[corrected] 589,081 rows, from 1996.**
**Grain:** one row per (`raceId`, `driverId`, `lap`). **Primary key:** (`raceId`, `driverId`, `lap`).

| Column | Meaning |
| --- | --- |
| `raceId`, `driverId` | Race and driver |
| `lap` | Lap number |
| `position` | Running position at the end of that lap |
| `time` | Lap time as text like `1:27.452` (convert to seconds) |
| `milliseconds` | Lap time in milliseconds |

**Relations:** `raceId` -> `races`; `driverId` -> `drivers`.
**Pre-race usable?** No. Race data. Useful for exploration only.

---

### `pit_stops`
**Represents:** every pit stop made during races. **11,371 rows, from 2011.**
**Grain:** one row per (`raceId`, `driverId`, `stop`). **Primary key:** (`raceId`, `driverId`, `stop`).

| Column | Meaning |
| --- | --- |
| `raceId`, `driverId` | Race and driver |
| `stop` | Stop number for this driver in this race |
| `lap` | Lap on which the stop happened |
| `time` | Time of day of the stop |
| `duration` | Time spent in the pit lane, as text. Mostly seconds (`26.898`), but long stops are written as minutes (`16:44.718`), so convert carefully |
| `milliseconds` | Duration in milliseconds |

**Relations:** `raceId` -> `races`; `driverId` -> `drivers`.
**Pre-race usable?** No. Race data.

---

## Relationship map

```
circuits ──< races >── seasons
               │
   ┌───────────┼───────────────┬──────────────────┐
   │           │               │                  │
results     qualifying    driver_standings    lap_times / pit_stops
sprint_results             constructor_standings
constructor_results
   │  │  │
   │  │  └── status        (results, sprint_results via statusId)
   │  └───── constructors  (results, qualifying, sprint_results,
   │                        constructor_results, constructor_standings)
   └──────── drivers       (results, qualifying, sprint_results,
                            driver_standings, lap_times, pit_stops)
```

`A ──< B` means one row in A links to many rows in B. For the full diagram with cardinalities, see `F1_EERD.svg` / `F1_EERD.md`.

### Foreign-key summary (23 links, all verified: 0 orphans, 0 nulls)

| Child table | Column | Parent table |
| --- | --- | --- |
| `races` | `circuitId` | `circuits` |
| `races` | `year` | `seasons` |
| `results` | `raceId` | `races` |
| `results` | `driverId` | `drivers` |
| `results` | `constructorId` | `constructors` |
| `results` | `statusId` | `status` |
| `qualifying` | `raceId`, `driverId`, `constructorId` | `races`, `drivers`, `constructors` |
| `sprint_results` | `raceId`, `driverId`, `constructorId`, `statusId` | `races`, `drivers`, `constructors`, `status` |
| `driver_standings` | `raceId`, `driverId` | `races`, `drivers` |
| `constructor_standings` | `raceId`, `constructorId` | `races`, `constructors` |
| `constructor_results` | `raceId`, `constructorId` | `races`, `constructors` |
| `lap_times` | `raceId`, `driverId` | `races`, `drivers` |
| `pit_stops` | `raceId`, `driverId` | `races`, `drivers` |

### [added] How we know these are foreign keys
1. **Name:** the column has the same name as another table's primary key.
2. **Meaning:** it describes a link and repeats in the child table (many rows -> one parent row).
3. **Data:** every value exists in the parent's primary key (0 orphans). Checked in notebook cell 2.2.

The data check alone is not enough: columns like `lap_times.position` or `races.round` contain small numbers that also happen to exist as IDs in other tables, so they pass a value check without being links.

---

## Which tables answer which question

| Question | Tables to join |
| --- | --- |
| Q1: front-row start -> podium by circuit, before/after 2014 | `results` + `qualifying` + `races` + `circuits` |
| Q2: home-country advantage, controlling for grid position | `results` + `drivers` + `races` + `circuits` (+ a nationality-to-country mapping) |
| Q3: mechanical-retirement rate by constructor, 2014-2021 vs. 2022-2024 | `results` + `status` + `races` + `constructors` |
| Modeling table | `results` (base) + `races` + `qualifying` + shifted `driver_standings` / `constructor_standings` + past-race form from `results` |

## Quick leakage guide

| Safe (known before the race) | Never (known only after the race) |
| --- | --- |
| IDs, `grid`, `qualifying` positions and times, circuit and driver static info, **shifted** standings, **past-race** form | `positionOrder` (except as the target), `position`, `points`, `laps`, `time`, `statusId`, fastest-lap columns, `lap_times`, `pit_stops`, same-race `constructor_results`, unshifted standings |
