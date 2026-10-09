# F1 Podium Prediction Project: Explained Step by Step

A plain-language guide to the project, built from the two PDFs, the 14 CSV files, and the questions asked along the way. Numbers marked **(verified)** were checked directly against our CSVs.

## Contents
1. [The project in one minute](#1-the-project-in-one-minute)
2. [PDF 1: "Formula 1 for Newcomers", step by step](#2-pdf-1-formula-1-for-newcomers-step-by-step)
3. [Your questions, answered](#3-your-questions-answered)
4. [The CSV files, one by one](#4-the-csv-files-one-by-one)
5. [How the tables connect](#5-how-the-tables-connect)
6. [PDF 2: the Milestone 1 brief, step by step](#6-pdf-2-the-milestone-1-brief-step-by-step)
7. [Problems found in the data (verified)](#7-problems-found-in-the-data-verified)
8. [Decisions not taken yet](#8-decisions-not-taken-yet)
9. [Quick glossary](#9-quick-glossary)

---

## 1. The project in one minute

| Item | Answer |
|---|---|
| **Goal** | For every driver in a race, predict whether they finish in the **top 3 (the podium)** |
| **Unit of analysis** | One driver in one race (one row = one prediction) |
| **Target** | `positionOrder <= 3` (podium = 1, otherwise 0) |
| **Cutoff** | Only use information known **after qualifying and before the race starts** |
| **Forbidden** | Anything known only during or after the race. Using it is **data leakage** |
| **Data** | Kaggle/Ergast Formula 1 dataset, 1950-2024, 14 linked CSV files |
| **Deadline** | 18 October 2026, 11:59 PM |

```
Friday            Saturday            [CUTOFF]            Sunday
Practice  -->  Qualifying  -->  Grid is fixed  -->  Race  -->  Results
(not in data)   (allowed)         (allowed)          (forbidden from here on)
```

Everything to the left of the cutoff can be a feature. Everything to the right is leakage.

---

## 2. PDF 1: "Formula 1 for Newcomers", step by step

This PDF teaches just enough F1 to understand the data and to recognise leakage.

### Step 1: What F1 is
- A world championship of single-seat racing cars, run every year since 1950.
- Each year is a **season**. A season is made of individual races called **Grands Prix**, held at different **circuits** (tracks).
- **Drivers** are the people in the cars. **Constructors** are the teams that build and run the cars (Ferrari, McLaren, Mercedes, Red Bull).
- Today each team enters **2 cars**, so a modern race has about 20 drivers. In the 1950s-80s the fields were much larger and less uniform.

### Step 2: Two championships
Both are decided by points:
- **Drivers' Championship:** points go to the individual driver.
- **Constructors' Championship** (since 1958): the points of a team's cars are added together.

### Step 3: What a podium is
A podium is a finish in **1st, 2nd or 3rd**, named after the stand where the top three receive trophies. It's rare by design: about 3 of 20 drivers per race, roughly **15%** of rows in the modern era, and much less when 30+ cars entered.

### Step 4: What decides who wins
A mix of car performance (the biggest factor in most eras), driver skill, starting position, strategy, reliability and luck. That is why our features lean on **grid position and constructor form**, not just driver form.

### Step 5: The race weekend (where the cutoff sits)

| # | Stage | What happens | Usable as a feature? |
|---|---|---|---|
| 1 | **Practice** (Fri) | Free sessions to tune the car, no points | Not in the dataset anyway |
| 2 | **Qualifying** (Sat) | Timed laps. Fastest driver gets **pole position** (P1). P1 and P2 form the **front row** | **Yes** |
| 3 | **Starting grid** | Normally the qualifying order, but penalties, pit-lane starts or exclusions can change it | **Yes** |
| 4 | **Race** (Sun) | Standing start, about 305 km, pit stops for tyres. First three across the line are on the podium | **No** |
| 5 | **Results** | Finishing order, points, reason for stopping (status), updated standings | **No** (all post-race) |

**Our prediction is made between stage 3 and stage 4.**

### Step 6: Sprint weekends
From 2021, a few races per season add a short Saturday race (a **sprint**, about 100 km, fewer points). The format changed:
- **2021-2022:** the sprint finishing order set Sunday's grid.
- **2023 onward:** Friday qualifying sets Sunday's grid, and a separate sprint qualifying sets the sprint's own grid.

The sprint happens before the main race, so its result is technically pre-race information. Whether to use it is a judgement call. (More in [Section 3, Q3](#q3-what-is-a-sprint-and-what-does-it-set-the-sunday-grid-mean).)

### Step 7: Glossary terms, grouped by what they mean for us

**Allowed features (known pre-race)**
| Term | Meaning | Note |
|---|---|---|
| Grid position | Where the car actually starts, after penalties | `0` in the data supposedly means a pit-lane start, to verify |
| Pole position | First place on the grid, earned by the fastest qualifying lap | "Strongest single predictor of a podium" |
| Qualifying | Timed session that sets the starting order | Patchy coverage for older years |
| Standings | Cumulative points and rank after each race | Only usable once shifted to "before this race" |

**Forbidden (post-race)**
Fastest lap, pit stops, status, DSQ (disqualification after the race), points won in this race, laps completed. Safety cars and tyre compounds are background only.

**Concepts that affect how we handle the data**
| Term | Meaning | Why it matters |
|---|---|---|
| Classified | Completed at least 90% of the winner's laps, so gets an official position even if the car stopped | Explains why some retired drivers still have a numeric position |
| Lapped (+1 Lap) | Finished but one or more laps behind | Counts as finished, not a retirement |
| DNF / Retirement | Did Not Finish. Split into mechanical (engine, gearbox) and accident/driver causes | Question 3 |
| DNQ / DNPQ | Did Not (Pre-)Qualify: too slow to earn a grid place | Rows with no race start; must decide if they belong in the table |
| Constructor | The team. Renamed teams get a new `constructorId` | Team history can break |
| Home race | Race in the driver's own country | Question 2; needs nationality-to-country mapping |
| Hybrid era | 2014-2021 rules (1.6L turbo V6 + energy recovery) | Era split for Questions 1 and 3 |
| DRS | Rear-wing flap that eases overtaking, from 2011 | Grid matters slightly less afterwards |
| Season | One championship year | Split: train <= 2019, validation 2020-2021, test >= 2022 |

### Step 8: How a result is recorded (`results.csv`)
Three position columns describe where a driver finished. They are easy to confuse:

| Column | What it holds | Example: driver who crashed out |
|---|---|---|
| `position` | Official finishing place; empty (`\N`) if not classified | `\N` |
| `positionText` | Place as text, or a letter code | `R` |
| `positionOrder` | A full ranking of **every** entrant, always filled | `17` |

**Our target uses `positionOrder`** because it is the only one filled for every row. Letter codes: **R** retired, **D** disqualified, **E** excluded, **W** withdrawn, **F** failed to qualify, **N** not classified.

The `status` column (via `status.csv`) says why a race ended. "Finished", "+1 Lap", "+2 Laps" mean the driver reached the flag. Everything else (over 100 reasons) is a cause of stopping. For Question 3 we must group these ourselves into **mechanical failures** (Engine, Gearbox, Hydraulics, Brakes, Power Unit...) versus **accidents, driver errors and other causes**, and document the mapping.

A podium is almost always a clean lead-lap finish, but a post-race disqualification can promote the 4th-place driver. `positionOrder` already reflects the final, post-appeal classification. **(verified:** in the 1983 Brazilian GP, 13 rows have `position` different from `positionOrder` because of disqualifications.)

### Step 9: Qualifying formats through history

| Seasons | Format | What the dataset shows |
|---|---|---|
| 2006-2024 | Three-part knockout: Q1, Q2, Q3 | `q1`, `q2`, `q3`; knocked-out drivers have `\N` in later parts |
| 2005 | Single-lap runs | Mostly `q1` only |
| 2003-2004 | Single-lap, one car on track at a time | Mostly `q1` only |
| 1996-2002 | One-hour session, "107% rule" | Mostly `q1` only |
| 1950-1995 | Varied formats | Little or no qualifying data |

For most of history the `grid` column in `results.csv` is the only record of the starting order. This causes **qualifying-coverage drift** (explained in [Section 3, Q6](#q6-qualifying-coverage-drift)).

### Step 10: Technical and sporting eras

| Era | What defined it | Who tended to win |
|---|---|---|
| 1950-57 | Front-engine cars, few safety rules, very high retirement | Alfa Romeo, Ferrari, Maserati, Mercedes |
| 1958-65 | Rear-engine revolution; Constructors' title starts 1958 | Cooper, Lotus, BRM, Ferrari |
| 1966-76 | 3-litre engines, wings from 1968, customer Cosworth engine | Lotus, Tyrrell, Ferrari, McLaren |
| 1977-88 | Turbos and ground effect; refuelling banned from 1984 | McLaren, Williams |
| 1989-94 | Turbos banned; driver aids banned 1994; safety car 1993 | McLaren-Honda, then Williams-Renault |
| 1995-2008 | V10 then V8 engines; in-race refuelling (strategy central) | Williams, McLaren, then Ferrari/Schumacher |
| 2009-13 | Aero reset; DRS and single tyre supplier from 2011 | Brawn 2009, then Red Bull/Vettel |
| 2014-21 | Turbo-hybrid V6; wider cars 2017; 17-race 2020 | Mercedes (every constructors' title), Verstappen 2021 |
| 2022-24 | Ground-effect cars; budget cap | Red Bull 2022-23, McLaren 2024 constructors' |

Season length grew from 7 races (1950) to 24 (2024), and modern cars are far more reliable. So "typical" podium and retirement rates change by era. The project is **era-sensitive**.

### Step 11: Oddities of early F1 that break assumptions
1. **Shared drives** (until 1957): a team could hand a car to a teammate mid-race and split the points. The same driver then has two result rows in one race, or two drivers share one car's result. This breaks our required grain of one row per (`raceId`, `driverId`).
2. **Indianapolis 500** (1950-1960): counted as a championship race, but almost no F1 regulars entered.
3. **Oversized, uneven fields:** privateers, one-off local drivers, many more cars than places on the grid.
4. **Identity drift:** drivers switched teams freely, car numbers weren't fixed, constructors changed names.
5. **Low reliability:** far higher retirement rates in the early decades.

Each of these is explained with examples in Section 3.

---

## 3. Your questions, answered

### Q1: Are there only 2 seasons (1950 and 2024)? What is a Grand Prix?

**No: there are 75 seasons**, one per year from 1950 to 2024. I only named 1950 and 2024 as the two ends of the range.

- A **season** is one championship year. Points reset at the start of each season. Races per season grew over time: **7 in 1950, about 9-15 in the 1960s-70s, about 16-19 in the 2000s, 24 in 2024**.
- A **Grand Prix** is **one individual race** with an official name, held at a **circuit** (the physical track). Examples: "British Grand Prix" (race in Britain), "Monaco Grand Prix". The same name repeats across years, but each one is a different race with its own `raceId`.

**In our data:** `seasons.csv` has 75 rows (one per year). `races.csv` has **1,125 rows** (one per Grand Prix), each with a `year` and `round`. That averages about 15 races per season.

```
Season (year)                      e.g. 2024
  └── Grand Prix / race (raceId)   e.g. Bahrain GP (round 1) ... Abu Dhabi GP (round 24)
        └── Driver entry           one row per driver in results.csv (about 20)
```

### Q2: Does each team have 2 cars? Does 20 drivers mean 10 contestants?

Yes: each team enters **2 cars, each with its own driver**. There are two kinds of contestants:
- **Drivers:** about 20 per race. Each gets their own result.
- **Teams (constructors):** about 10 per race.

So 10 teams x 2 cars = 20 drivers. `results.csv` has **one row per driver** (about 20 per race), and each row has a `constructorId` for the team.

Teammates also compete **against each other**, since both are fighting for the same top-3 places. That is why a podium is "3 of 20 spots", not "3 of 10".

**What we predict:** one answer per **driver** per race ("will this driver finish top 3?"). Teams still matter as a feature, because a driver's chances depend heavily on how good their car is (constructor form).

The "2 cars per team" rule is modern. In the 1950s-80s, teams entered varying numbers of cars, and fields reached 30+.

### Q3: What is a sprint, and what does "it sets the Sunday grid" mean?

**A normal weekend:** Friday practice, Saturday qualifying (sets the grid), Sunday race.

**A sprint weekend** (a few races per year since 2021) adds a short extra **Saturday race**:
- About 100 km (roughly a third of a normal race), no pit stop needed.
- Fewer points: top 8 only, 8 down to 1. **(verified:** the sprint `points` column only contains the values 0-8.)

"Sets the Sunday grid" means the sprint's finishing order decides where cars line up for Sunday's main race:

| Years | How the grids were set |
|---|---|
| **2021-2022** | Friday qualifying set the **sprint** grid. The **sprint result** then became **Sunday's grid** (e.g. finish 3rd in the sprint, start Sunday 3rd, apart from penalties) |
| **2023 onward** | Friday qualifying sets **Sunday's** grid as normal. A separate Saturday "sprint qualifying" sets the **sprint's** grid only |

**Why it matters to us:**
1. The sprint is **pre-race information** (it ends before Sunday), so using it isn't leakage. Whether to use it is a judgement call.
2. In 2021-22, qualifying did not set the Sunday grid, so `grid` and qualifying position can differ more.
3. There's very little sprint data: only **18 races** (3 in 2021, 3 in 2022, 6 in 2023, 6 in 2024), all in `sprint_results.csv`. **(verified:** the sprint finish matched Sunday's grid 43% / 60% of the time in 2021 / 2022, and only 12% / 17% in 2023 / 2024, which fits the format change.)

### Q4: If the sprint doesn't set the grid from 2023, what's the point of it?

It still has its own purposes:
1. **It awards points.** It's a real race with its own result. The points count toward both championships, so a driver can gain or lose ground in the title fight on Saturday.
2. **Entertainment.** Without it, Saturday has just qualifying. The sprint gives fans a second race, which is the main reason it was introduced. (General F1 background, not from our data or PDFs.)
3. **The 2023 change made it a standalone event.** Friday qualifying now matters for Sunday, and the sprint (with its own qualifying) is a separate mini-competition.

**For our project:** Sunday's grid is built from Friday qualifying plus penalties, with no direct input from the sprint. But a driver's Saturday performance might still carry information, and it is pre-race. The catch is that sprint data exists for only 18 of 1,125 races, so a sprint feature would be empty for almost every row.

### Q5: Points are per driver. Is the winner the person with the most points?

There are **two different kinds of "winner"**:

| | Race winner | Champion |
|---|---|---|
| **Who** | Driver who crosses the line first in a race | Driver with the most points at the end of the season |
| **Based on** | Finishing position in one race | Points added up across all races |
| **Sprint affects it?** | No | Yes, sprint points add to the total |

- Points are awarded per driver, per race, by finishing position. Modern era: 25 for a win, then 18, 15, 12, 10, 8, 6, 4, 2, 1 down to 10th. Older eras used smaller numbers. **(verified:** in our data a win is worth at most 9 points before 1990 and 10 from 1990.)
- Both of a team's drivers' points are added together for the **Constructors' Championship**.
- A driver can win fewer races but be champion by scoring more consistently.

**For our project:** the target is finishing position (`positionOrder <= 3`), and it doesn't use points. Points are only useful as a **past** feature, i.e. points accumulated before this race (see Q10).

### Q6: Qualifying coverage drift

"Coverage" = for a given race, do we have qualifying data for each driver? "Drift" = this changes over time. **(verified)**

| Years | Qualifying data in our CSV |
|---|---|
| 1950-1993 | **None** |
| 1994 | Most races (15 of 16) |
| 1995 | Full |
| 1996-2002 | **Partial**; 1999-2002 has under 25% of rows (e.g. 2001: only 1 of 17 races) |
| 2003-2024 | **Essentially complete** |
| `q2` column | Only from 2005 |
| `q3` column | Only from 2006 |

(The PDF guessed qualifying "begins in the mid-1990s". Our copy confirms **1994**.)

**The problem:** a qualifying feature (qualifying position, gap to pole) would be empty for about 60% of historical rows and filled for modern rows. A model trained on all years could learn "missing means old era" instead of anything real about qualifying.

**The three options the PDF names** (to be decided later):
1. **Impute** the missing values.
2. **Fall back to `grid`**, which exists for every year.
3. **Restrict the training window** to years with qualifying data.

Also note two small extras: there are 59 result rows in covered races without a qualifying row, and `q2`/`q3` use **empty strings** (not `\N`) in 22 and 46 cells, a second hidden kind of missing value.

### Q7: Indianapolis 500

The Indy 500 is a famous American oval race. From **1950 to 1960 it was officially counted as a Formula 1 championship race**, though it was almost a different sport. **(verified)**
- **11 races, 405 result rows.**
- Run by American teams (Watson, Epperly, Lesovsky and similar), on an oval, with up to **33 cars** on the grid and **200 laps**.
- Of the **107 drivers** who entered it, **104 never raced any other F1 race** in those years.

**Why it matters:**
- It adds rows from drivers with no other F1 history, so "driver form" can't be computed for them.
- For **Question 2** (home race), it makes American drivers appear to race "at home" very often, because the race is in the USA and so are its drivers. That would distort the home-advantage answer.
- Excluding it is defensible, as long as we document it.

### Q8: Oversized, uneven fields

A "field" is the group of cars entering a race. Today it's even: **about 20 entries and 20 starters per race**. In the late 1980s-early 1990s it wasn't. **(verified)**

| Years | Entries per race | Actual starters per race |
|---|---|---|
| 1989-1994 | **31.6** | **25.9** |
| 2022-2024 | **20.0** | **19.9** |

In 1989-94 there were 541 rows with "Did not qualify" or "Did not prequalify": drivers who entered but never raced. There were also privateers (people entering their own car) and one-off local drivers.

**Effects on the data:**
- Those rows exist in `results.csv` but the driver never started, so they can never reach the podium. They push the podium rate **down**: **9.5% in 1989-94, versus 15.0% in 2022-24**.
- Their `grid` is `0`, which looks like a pit-lane start but really means "never started".
- We must decide whether such rows belong in the modeling table.

### Q9: Identity drift and low reliability

**Identity drift** means the identifiers (team names, driver teams, car numbers) **aren't stable over time**, so history is hard to follow.

- **Teams change names.** Toleman became Benetton, then Renault, Lotus F1, then Alpine. In our data each name has its own `constructorId`, so a "this team's recent form" feature **resets to zero** at every rename, even though it is the same garage. Many different teams are also called "Lotus" (Team Lotus, Lotus-Climax, Lotus F1...), which aren't all the same team.
- **Drivers moved more.** **(verified)** In the 1960s, **17.4%** of drivers raced for more than one team in the same season, versus about **2%** in the 2020s.
- **Car numbers weren't fixed.** **(verified)** In the 1960s, **54%** of driver-seasons used more than one car number, versus about **1%** today. So `number` can't be used as an identifier.

**Takeaway:** follow `constructorId` and `driverId`, and accept that renames reset history.

**Low reliability** means how often a car actually makes it to the end. Early cars broke down a lot. **(verified)** Share of starters who finished (including "+N laps"):

| Era | Finish rate |
|---|---|
| 1950-57 | 51% |
| 1976-88 | 46% |
| 1994-2008 | 62% |
| 2014-2021 | 82% |
| 2022-2024 | 86% |

In the 1970s-80s about **half** of the starters didn't finish, so starting on pole meant much less: an engine failure could end your race. Today a good grid slot converts to a podium far more reliably. **(verified:** pole gives about 50% podium in 1950-80 and about **81%** in 2014-21.) A model trained on all history can therefore misjudge the modern era.

### Q10: "Standings really do include the current race, which is why they must be shifted"

**Standings** are a table of each driver's **total** points and rank **after** each race. The word "after" is the catch.

A real example from our data, driverId 830 (Max Verstappen), 2023:

| Standings row for | Standings points | Points won in that race |
|---|---|---|
| Round 2, Saudi Arabian GP | 44 | 19 |
| Round 3, Australian GP | **69** | 25 |

69 = 44 + 25. The "Round 3" standings row already contains the 25 points won **in Round 3 itself**.

If we predict the Australian GP and use that row as a feature, we hand the model "69 points", which already includes the race result. That is **leakage**: the model learns "big jump in points = good finish" and looks brilliant for the wrong reason.

**The fix: shift the standings back by one race.** Use the previous round's row (44 points). For round 1 of a season, use the last race of the previous season, or treat it as 0.

**(verified:** standings include the same-race points in about 99.4% of rows, and the round-1 standing equals the race points in 100% of cases.)

### Q11: Pole position vs grid position

| | Pole position | Grid position |
|---|---|---|
| **What it is** | Result of **qualifying**: the driver with the fastest lap | Where the car **actually starts** the race |
| **Decided by** | Lap time | Qualifying order **plus** penalties, pit-lane starts, exclusions |
| **Data column** | `qualifying.position` (`qualifying.csv`) | `grid` (`results.csv`) |

**Example:** Driver A sets the fastest lap (pole) but gets a 5-place grid penalty. A's qualifying position is **1**, A's grid position is **6**, and the driver who qualified 2nd now starts **1st** on the grid.

**(verified)** In rows where both exist, they match only **76.7%** of the time. About **5.1%** of drivers start lower than they qualified (penalties), and about **18.2%** start higher (others were penalised or didn't start).

**Why it matters:** pole/grid 1 is the strongest single predictor (about 81% podium in 2014-21). Question 1 requires us to distinguish them. Both are allowed features. `grid = 0` is a special case (see Section 7).

---

## 4. The CSV files, one by one

14 tables, all comma-separated, with the literal text `\N` used as a placeholder for missing values (a **sentinel**; it must be converted to real missing values). Row counts exclude the header. **(verified)**

### Core tables

#### `races.csv`: 1,125 rows, the spine of the dataset
One row per Grand Prix. Key: `raceId`.

| Column(s) | Meaning |
|---|---|
| `raceId` | Unique race id; used by almost every other table |
| `year`, `round` | Season and race number within it (1-24) |
| `circuitId` | Which track (links to `circuits.csv`) |
| `name`, `date`, `time` | e.g. "British Grand Prix", race date, start time (`time` only exists from 2005) |
| `fp1_*`, `fp2_*`, `fp3_*`, `quali_*`, `sprint_*` | Session dates/times; almost all `\N` before 2021 |

#### `results.csv`: 26,759 rows, one row per driver per race
This is where the **target** comes from. Key: `resultId`. **The real grain is (`raceId`, `driverId`), which is not unique** (see Section 7).

| Column | Meaning | Pre-race? |
|---|---|---|
| `resultId`, `raceId`, `driverId`, `constructorId` | Identifiers | Yes |
| `number` | Car number | Yes (but unstable early on) |
| `grid` | Actual starting position (`0` = pit lane **or** never started) | **Yes, allowed** |
| `position` | Official place; `\N` if not classified (10,953 of them) | No |
| `positionText` | Place or letter code (R, D, E, W, F, N) | No |
| **`positionOrder`** | **Full ranking, always filled. Target source** | No (it **is** the answer) |
| `points`, `laps` | Points won, laps completed | No |
| `time`, `milliseconds` | Race time or gap to winner | No |
| `fastestLap`, `rank`, `fastestLapTime`, `fastestLapSpeed` | Fastest-lap data | No |
| `statusId` | Why the race ended (links to `status.csv`) | No |

#### `qualifying.csv`: 10,494 rows (494 races, 1994-2024)
Key: `qualifyId`. One row per driver per qualifying session.

| Column | Meaning |
|---|---|
| `raceId`, `driverId`, `constructorId`, `number` | Identifiers |
| `position` | Final qualifying rank |
| `q1`, `q2`, `q3` | Lap times as text like `1:26.572`, to be converted to seconds. `q2`/`q3` are `\N` for knocked-out drivers (and sometimes an empty string) |

**All pre-race, so allowed.** Coverage is the big limitation (Q6).

#### `drivers.csv`: 861 rows
Key: `driverId`.

| Column | Meaning |
|---|---|
| `driverRef`, `forename`, `surname`, `code` | Names and 3-letter code (`HAM`); `code` is `\N` for 757 drivers |
| `number` | Permanent number (modern era only; `\N` for 802) |
| `dob` | Date of birth (all parse; usable for age) |
| `nationality` | e.g. "British"; needed for **Q2** (home race) |

#### `constructors.csv`: 212 rows
Key: `constructorId`. Columns: `constructorRef`, `name`, `nationality`. Each rename of a team has its own id (identity drift).

#### `circuits.csv`: 77 rows
Key: `circuitId`. Columns: `circuitRef`, `name`, `location`, `country`, `lat`, `lng`, `alt`. Needed for Q1 (which circuit) and Q2 (circuit country).

#### `status.csv`: 139 rows
Key: `statusId`. Maps each id to a text such as "Finished", "+1 Lap", "Engine", "Collision". Post-race; used only for **Q3**.

### Standings tables (cumulative, **include the current race**)

#### `driver_standings.csv`: 34,863 rows
Key: `driverStandingsId`. Columns: `raceId`, `driverId`, `points`, `position`, `positionText`, `wins`. The totals **after** each race (must be shifted by one race to be safe).

#### `constructor_standings.csv`: 13,391 rows (from 1958)
Key: `constructorStandingsId`. Same idea per team: `raceId`, `constructorId`, `points`, `position`, `positionText`, `wins`.

#### `constructor_results.csv`: 12,625 rows (from 1958)
Key: `constructorResultsId`. A team's points **in a single race** (`raceId`, `constructorId`, `points`, `status`). `status` is `\N` except for 17 rows marked `D`. Post-race.

### Special-case tables

#### `sprint_results.csv`: 360 rows (18 races, 2021-2024)
Same style as `results.csv` (grid, position, points, laps, time, `statusId`...) but for the short Saturday race. Pre-race relative to Sunday, but tiny.

#### `seasons.csv`: 75 rows
Columns: `year`, `url`. Essentially a lookup list of years.

### Post-race detail tables (never features)

#### `pit_stops.csv`: 11,371 rows (2011-2024)
Key: (`raceId`, `driverId`, `stop`). Columns: `lap`, `time`, `duration`, `milliseconds`. Happens during the race.

#### `lap_times.csv`: 589,081 rows (1996-2024)
Key: (`raceId`, `driverId`, `lap`). Columns: `position`, `time`, `milliseconds`. The biggest file; every lap of every driver. Happens during the race.

---

## 5. How the tables connect

```
                    seasons (year)
                         |
circuits (circuitId) --- races (raceId) -------------------------------+
                         |                                              |
     +-------------------+---------+----------------+--------------+    |
     |                             |                |              |    |
 results  <---(raceId,driverId)--> qualifying   driver_standings  sprint_results
     |                             |                |
     |--- drivers (driverId)       +--- constructors (constructorId)
     |--- constructors (constructorId)
     |--- status (statusId)

 constructor_standings, constructor_results  --> races + constructors
 pit_stops, lap_times                        --> races + drivers
```

**How to join (for the modeling table):**
- Start from `results` (one row per driver per race) and attach `races` (year, round, circuit).
- Attach `qualifying` on (`raceId`, `driverId`).
- Attach **previous-race** standings on the driver and on the constructor.
- Attach `drivers` (nationality, dob) and `circuits` (country) for Q2.
- `status` is used only for Question 3.

**Integrity check (verified):** all 14 primary keys are unique and non-null, and all 23 foreign-key relationships have **zero orphans**. Every race has results. No table has full-row duplicates. The messy part is the grain of `results`, not the links.

---

## 6. PDF 2: the Milestone 1 brief, step by step

### Step 1: Introduction
F1 produces rich, relational data. Which drivers have a realistic shot at the podium is largely determined before the lights go out. The skill being tested is **careful feature engineering and leakage control**, which matter as much as model choice, because results, points and status are only known after the race.

### Step 2: The dataset
- Kaggle/Ergast "Formula 1 World Championship" dataset, 1950-2024, **14 linked tables** (so you must **join** several to answer most questions).
- **Unit of analysis:** one driver entering one race.
- **Target:** podium (`positionOrder <= 3`).
- **Cutoff:** after qualifying, before the race starts. Current-race results, status, points, laps, pit stops and post-race standings are **not allowed** (leakage). Part of the task is learning to spot "future" fields yourself (Questions 4 and 5 in the original text).

### Step 3: Project objectives

**1. Data cleaning and auditing**
- **EDA before and after cleaning**, with proper visualisations, to show the impact of cleaning.
- Clean `\N` sentinels; convert dates to real dates and lap-time strings to seconds.
- **Exactly one row per (`raceId`, `driverId`).** Check for duplicates (shared drives), choose a rule, apply it, explain why.
- Verify primary keys are unique and non-null, and foreign keys all reconcile. **Raw CSVs stay unchanged**; clean copies only.
- EDA must be backed by code and justification, not manual inspection.

**2. Three data-engineering questions** (each needs multi-hop joins, a visualisation, and a short note on grain, missingness and the pre-race cutoff)
1. **Which circuits convert a front-row start into a podium most often, and does the ranking change after 2014?** Distinguish qualifying position from grid.
2. **Do drivers podium more often at their home circuit, after controlling for starting position?** Compare drivers from similar grid slots, so the effect isn't just home drivers qualifying better.
3. **Which constructors have the highest mechanical-retirement rate in 2014-2021 vs 2022-2024?** "Mechanical" = a component failed. It excludes crashes, driver errors and regulation decisions.

**3. Feature selection and engineering**
- Justify each feature with evidence (plots, correlations or recorded experiments).
- Use a proper train/validation/test split and justify it.
- The exact feature list and encoding are your choice; document the reasoning.

**4. Predictive modeling**
Train and compare, on the same rows and same features:
- **At least two statistical ML models** (e.g. logistic regression, random forest, gradient boosting).
- **A shallow neural network** (about 1-2 hidden layers), using a standard library.
- Binary classification (podium vs not). Metrics: **ROC-AUC** (class separation), **PR-AUC** (better when positives are rare), **F1** (balance of precision and recall at a threshold).
- Report on training/validation **and** on the unseen test set. **Thresholds and hyperparameters must be chosen on train/validation only, never on the test set.**

**5. Experiments**
- **Feature-group ablation:** remove one group of features at a time (e.g. all form features, all qualifying features) and retrain, to measure how much each group really contributes.

**6. Model explainability (XAI)**
- **Global:** permutation importance and SHAP.
- **Local:** at least one single-prediction explanation (LIME or a SHAP waterfall/force plot).
- Plot and interpret everything. **State explicitly that explanations are not causal effects.**

### Step 4: Deliverables
1. One **run-all Jupyter notebook** with everything: audit, cleaning, data-engineering answers, features, modeling, experiments, XAI, and an inference function. It must be sectioned and every conclusion backed by evidence.
2. EDA with plots.
3. A unique driver-race modeling table, with documented duplicate handling and leakage-safe form/standings/grid/qualifying features.
4. A **model comparison table** (statistical models and the shallow NN) with all metrics on validation and test, and the primary/secondary metric justified.
5. Feature-group ablation results and **at least two preprocessing-order experiments**.
6. Global and local explanations.
7. An **inference function** demonstrated on a complete record and a partially missing record.
8. An **analytical report** (PDF): written answers to the three questions with figures, selected features and why each is valid pre-race, and known limitations (qualifying-coverage drift, era sensitivity).

### Step 5: What to expect at the evaluation
- **Every team member must be able to answer about any step.**
- "An AI tool suggested it" is not a justification.
- Two valid ways to justify a step: **hypothesis-driven** (EDA shows X, so we did Y) or **trial-and-error** (before/after baseline, each attempt in its own cell).
- Compare multiple approaches; the notebook should show **at least three distinct modeling attempts**.
- A **baseline** is required (a simple statistical model or shallow FFNN).
- The notebook must be **run-all ready** with clear markdown explanations.

### Step 6: Submission
Deadline **18 October 2026, 11:59 PM**. Submit via the form: a link to the Kaggle notebook, a GitHub repo link, and the report as a PDF.

### Things I noticed in the brief
- The deliverables mention "all five metrics from Section 4", but Section 4 lists only **three** (ROC-AUC, PR-AUC, F1). We may want to add more (e.g. precision, recall) or ask.
- The dataset link says "1950-2020", but the brief (and our CSVs, which reach 2024) cover 1950-2024. **(verified:** our data has races up to Abu Dhabi 2024.)
- The text says local explanation can be LIME **or** local SHAP, but the checklist says "LIME". Doing both is the safe choice.

---

## 7. Problems found in the data (verified)

| # | Problem | Evidence |
|---|---|---|
| 1 | **Duplicate (`raceId`, `driverId`) rows** | 85 groups = 176 rows, 1950-1964 plus one 1978 case |
| 2 | The brief's "non-zero grid" rule doesn't resolve them | In 82 of 85 groups, both rows have a non-zero grid |
| 3 | The two duplicate rows can disagree on the podium label | 21 of 85 groups |
| 4 | Different drivers sharing one car's result | 228 rows; 18 races have 4, 5 or 7 podium rows |
| 5 | `grid = 0` is overloaded | 95.6% are non-starters; true pit-lane starts only 2015-2024 (72 rows) |
| 6 | Non-start rows (DNQ/DNPQ/Withdrew/107%) | 1,613 rows (about 6%), zero podiums, mostly 1957-1994 |
| 7 | Qualifying coverage drift | None before 1994, patchy to 2002, complete from 2003 |
| 8 | Hidden missing values | Empty strings in `q2` (22) and `q3` (46), besides `\N` |
| 9 | Standings include the current race | 99.4% of rows |
| 10 | Messy labels | `USA` and `United States`; `'Argentinian '` with a trailing space; dual nationalities; `Lotus-Pratt &amp; Whitney` |
| 11 | Team rebrands split history | Force India -> Racing Point -> Aston Martin, Toro Rosso -> AlphaTauri -> RB, Lotus/Renault/Alpine, etc. |
| 12 | Very little sprint data | 18 races (2021-2024) |

Other useful facts: the overall podium rate is **12.7%**; 3,231 podium rows are "Finished" and 128 are "+1 Lap".

**Podium rate by grid slot (1st / 2nd / 3rd):**

| Years | Grid 1 | Grid 2 | Grid 3 |
|---|---|---|---|
| 1950-1980 | 50% | 47% | 39% |
| 2001-2013 | 77% | 59% | 46% |
| 2014-2021 | 81% | 71% | 59% |
| 2022-2024 | 79% | 72% | 44% |

---

## 8. Decisions not taken yet

You asked to understand everything before deciding anything. None of these has been decided:

1. **How to resolve duplicate (`raceId`, `driverId`) rows** from shared drives.
2. **Which seasons to model** (full history vs. only years with qualifying).
3. **Whether to keep or drop** non-start rows and the Indianapolis 500.
4. **Whether to use sprint data** as features.
5. Also pending: the nationality-to-country map (Q2), the status-to-"mechanical" map (Q3), how to handle team lineages, how to treat `grid = 0`, the primary/secondary metric, and the "five metrics" question.

---

## 9. Quick glossary

| Term | One-line meaning |
|---|---|
| Season | One championship year (75 of them: 1950-2024) |
| Grand Prix | One race (1,125 in total) |
| Circuit | The physical track |
| Driver / Constructor | The person / the team |
| Podium | Finishing 1st, 2nd or 3rd (our target) |
| Pole position | Fastest qualifying lap; first on the grid *unless* penalised |
| Grid position | Where the car actually starts |
| Front row | Grid positions 1 and 2 |
| Sprint | Short extra Saturday race (2021+), few races |
| Standings | Cumulative points after each race |
| Classified | Completed >= 90% of the winner's laps |
| DNF / DNQ / DNPQ | Did not finish / did not qualify / did not pre-qualify |
| Status | Reason the race ended; post-race |
| Sentinel (`\N`) | Placeholder text meaning "missing" |
| Leakage | Using information that wouldn't exist at prediction time |
| Grain | What one row represents (here: one driver in one race) |
| Coverage drift | Data availability changing across time (e.g. qualifying) |
| Identity drift | Names/teams/numbers changing across time |
| Ablation | Removing a feature group and retraining to measure its contribution |
| XAI | Explainable AI (permutation importance, SHAP, LIME) |
