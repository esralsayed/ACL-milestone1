# retrievals/templates.py
# Each template: name -> intent, required params, optional params, scope note, Cypher.
# The Cypher strings have no ';' at the end and no '//' comments.

TEMPLATES = {}


def _t(name, intent, required, optional, scope, cypher):
    TEMPLATES[name] = {
        "intent": intent,
        "required": required,
        "optional": optional,
        "scope": scope,
        "cypher": cypher,
    }


# ===================== 1. driver_performance =====================
_t("driver_season_stats", "driver_performance", ["driver_id", "year"], [],
   "Race points only; sprint-race points are not included, so totals can be lower than the official standings.",
   """
   MATCH (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)-[:IN_SEASON]->(s:Season {year: $year})
   RETURN d.forename + ' ' + d.surname AS driver, s.year AS season,
          count(r) AS entries, sum(r.points) AS points,
          sum(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS wins,
          sum(CASE WHEN r.position <= 3 THEN 1 ELSE 0 END) AS podiums
   """)

_t("driver_totals", "driver_performance", ["driver_id"], ["year_from", "year_to"],
   "Race points only; sprint-race points are not included, so totals can be lower than the official figures. Wins and podiums are counted from race classification.",
   """
   MATCH (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)
   WHERE ($year_from IS NULL OR ra.year >= $year_from)
     AND ($year_to   IS NULL OR ra.year <= $year_to)
   RETURN d.forename + ' ' + d.surname AS driver, count(r) AS entries, sum(r.points) AS points,
          sum(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS wins,
          sum(CASE WHEN r.position <= 3 THEN 1 ELSE 0 END) AS podiums
   """)

_t("driver_at_circuit", "driver_performance", ["driver_id", "circuit_id"], ["before_date"],
   "Excludes did-not-qualify and withdrawn entries; average finish counts retirements as last.",
   """
   MATCH (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)-[:AT_CIRCUIT]->(c:Circuit {circuitId: $circuit_id}),
         (r)-[:HAS_STATUS]->(s:Status)
   WHERE NOT s.status IN ['Did not qualify', 'Did not prequalify', 'Withdrew']
     AND ($before_date IS NULL OR ra.date < date($before_date))
   RETURN d.forename + ' ' + d.surname AS driver, c.circuit_name AS circuit,
          count(r) AS starts,
          sum(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS wins,
          sum(CASE WHEN r.position <= 3 THEN 1 ELSE 0 END) AS podiums,
          avg(r.positionOrder) AS avg_finish
   """)

# ===================== 2. constructor_performance =====================
_t("constructor_totals", "constructor_performance", ["constructor_id"], ["year_from", "year_to"],
   "Race points only; sprint-race points are not included, so totals can be lower than the official standings. Counts every car entry, so a team has up to two entries per race."
,
   """
   MATCH (c:Constructor {constructorId: $constructor_id})<-[:FOR_CONSTRUCTOR]-(r:Result)-[:FOR_RACE]->(ra:Race)
   WHERE ($year_from IS NULL OR ra.year >= $year_from)
     AND ($year_to   IS NULL OR ra.year <= $year_to)
   RETURN c.constructor_name AS constructor, count(r) AS entries, sum(r.points) AS points,
          sum(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS wins,
          sum(CASE WHEN r.position <= 3 THEN 1 ELSE 0 END) AS podiums
   """)

_t("constructor_reliability", "constructor_performance", ["constructor_id"],
   ["year_from", "year_to", "before_date"],
   "Reliability = share of entries classified as Finished or lapped (+N laps).",
   """
   MATCH (c:Constructor {constructorId: $constructor_id})<-[:FOR_CONSTRUCTOR]-(r:Result)-[:FOR_RACE]->(ra:Race),
         (r)-[:HAS_STATUS]->(s:Status)
   WHERE ($year_from IS NULL OR ra.year >= $year_from)
     AND ($year_to   IS NULL OR ra.year <= $year_to)
     AND ($before_date IS NULL OR ra.date < date($before_date))
   WITH c, count(r) AS entries,
        sum(CASE WHEN s.status = 'Finished' OR s.status STARTS WITH '+' THEN 1 ELSE 0 END) AS classified
   RETURN c.constructor_name AS constructor, entries, classified,
          toFloat(classified) / entries AS reliability
   """)

_t("constructor_drivers", "constructor_performance", ["constructor_id", "year"], [],
   "Drivers with at least one race entry for the team that season.",
   """
   MATCH (c:Constructor {constructorId: $constructor_id})<-[:FOR_CONSTRUCTOR]-(r:Result)-[:BY_DRIVER]->(d:Driver),
         (r)-[:FOR_RACE]->(ra:Race)-[:IN_SEASON]->(:Season {year: $year})
   WITH c, d, count(r) AS races
   ORDER BY races DESC
   RETURN c.constructor_name AS constructor,
          collect(d.forename + ' ' + d.surname + ' (' + toString(races) + ' races)') AS drivers
   """)

# ===================== 3. head_to_head =====================
_t("teammate_race_h2h", "head_to_head", ["driver_a_id", "driver_b_id"], ["year_from", "year_to"],
   "Only races where both drove for the same team. 'Ahead' uses final classification order. Points are race points only, without sprint points.",
   """
   MATCH (a:Driver {driverId: $driver_a_id})<-[:BY_DRIVER]-(res_a:Result)-[:FOR_RACE]->(race:Race),
         (b:Driver {driverId: $driver_b_id})<-[:BY_DRIVER]-(res_b:Result)-[:FOR_RACE]->(race),
         (res_a)-[:FOR_CONSTRUCTOR]->(c:Constructor)<-[:FOR_CONSTRUCTOR]-(res_b)
   WHERE ($year_from IS NULL OR race.year >= $year_from)
     AND ($year_to   IS NULL OR race.year <= $year_to)
   RETURN a.surname AS driver_a, b.surname AS driver_b, c.constructor_name AS constructor,
          count(DISTINCT race) AS shared_races,
          sum(CASE WHEN res_a.positionOrder < res_b.positionOrder THEN 1 ELSE 0 END) AS a_ahead,
          sum(CASE WHEN res_b.positionOrder < res_a.positionOrder THEN 1 ELSE 0 END) AS b_ahead,
          sum(res_a.points) AS a_points, sum(res_b.points) AS b_points
   ORDER BY shared_races DESC LIMIT 5
   """)

_t("teammate_quali_h2h", "head_to_head", ["driver_a_id", "driver_b_id"], ["year_from", "year_to"],
   "Qualifying data starts in 1994; only sessions where both drove for the same team.",
   """
   MATCH (a:Driver {driverId: $driver_a_id})<-[:BY_DRIVER]-(qa:Qualifying)-[:FOR_RACE]->(race:Race),
         (b:Driver {driverId: $driver_b_id})<-[:BY_DRIVER]-(qb:Qualifying)-[:FOR_RACE]->(race),
         (qa)-[:FOR_CONSTRUCTOR]->(c:Constructor)<-[:FOR_CONSTRUCTOR]-(qb)
   WHERE ($year_from IS NULL OR race.year >= $year_from)
     AND ($year_to   IS NULL OR race.year <= $year_to)
     AND qa.position IS NOT NULL AND qb.position IS NOT NULL
   RETURN a.surname AS driver_a, b.surname AS driver_b, c.constructor_name AS constructor,
          count(DISTINCT race) AS shared_sessions,
          sum(CASE WHEN qa.position < qb.position THEN 1 ELSE 0 END) AS a_ahead,
          sum(CASE WHEN qb.position < qa.position THEN 1 ELSE 0 END) AS b_ahead
   ORDER BY shared_sessions DESC LIMIT 5
   """)

# ===================== 4. race_circuit_facts =====================
_t("race_podium", "race_circuit_facts", ["gp_name", "year"], [],
   "Top three finishers by final classification order.",
   """
   MATCH p = (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race {name: $gp_name, year: $year})
   WHERE r.positionOrder <= 3
   MATCH p2 = (r)-[:FOR_CONSTRUCTOR]->(c:Constructor)
   RETURN r.positionOrder AS position, d.forename + ' ' + d.surname AS driver,
          c.constructor_name AS constructor, ra.name AS race, ra.date AS date, p, p2
   ORDER BY position LIMIT 3
   """)

_t("circuit_info", "race_circuit_facts", ["circuit_id"], [],
   "Races held counts the Grands Prix in the data at this circuit.",
   """
   MATCH (c:Circuit {circuitId: $circuit_id})<-[:AT_CIRCUIT]-(ra:Race)
   RETURN c.circuit_name AS circuit, c.circuit_loc AS location, c.circuit_country AS country,
          count(ra) AS races_held, min(ra.year) AS first_year, max(ra.year) AS last_year
   """)

_t("top_winners_at_circuit", "race_circuit_facts", ["circuit_id"], [],
   "Wins by final classification, top five drivers.",
   """
   MATCH (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)-[:AT_CIRCUIT]->(c:Circuit {circuitId: $circuit_id})
   WHERE r.position = 1
   RETURN c.circuit_name AS circuit, d.forename + ' ' + d.surname AS driver, count(r) AS wins
   ORDER BY wins DESC LIMIT 5
   """)

# ===================== 5. qualifying_grid =====================
_t("pole_sitter", "qualifying_grid", ["gp_name", "year"], [],
   "Qualifying data starts in 1994.",
   """
   MATCH p = (d:Driver)<-[:BY_DRIVER]-(q:Qualifying)-[:FOR_RACE]->(ra:Race {name: $gp_name, year: $year})
   WHERE q.position = 1
   RETURN d.forename + ' ' + d.surname AS driver, ra.name AS race, q.q3 AS q3_time, p
   LIMIT 1
   """)

_t("driver_poles", "qualifying_grid", ["driver_id"], ["year_from", "year_to"],
   "Qualifying data starts in 1994; Q3 appearances count sessions with a recorded Q3 time.",
   """
   MATCH (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(q:Qualifying)-[:FOR_RACE]->(ra:Race)
   WHERE ($year_from IS NULL OR ra.year >= $year_from)
     AND ($year_to   IS NULL OR ra.year <= $year_to)
   RETURN d.forename + ' ' + d.surname AS driver, count(q) AS sessions,
          sum(CASE WHEN q.position = 1 THEN 1 ELSE 0 END) AS poles,
          sum(CASE WHEN q.q3 IS NOT NULL THEN 1 ELSE 0 END) AS q3_appearances
   """)

_t("grid_gains", "qualifying_grid", ["circuit_id", "year"], [],
   "Classified finishers who started from a grid slot; pit-lane starts excluded.",
   """
   MATCH (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race {year: $year})-[:AT_CIRCUIT]->(c:Circuit {circuitId: $circuit_id})
   WHERE r.grid > 0 AND r.position IS NOT NULL
   RETURN d.forename + ' ' + d.surname AS driver, ra.name AS race, r.grid AS grid,
          r.positionOrder AS finish, r.grid - r.positionOrder AS places_gained
   ORDER BY places_gained DESC LIMIT 5
   """)

# ===================== 6. pit_stops =====================
_t("fastest_pit_stops", "pit_stops", ["gp_name", "year"], [],
   "Pit stop data starts in 2011; duration is the time in the pit lane.",
   """
   MATCH p = (d:Driver)<-[:BY_DRIVER]-(ps:PitStop)-[:FOR_RACE]->(ra:Race {name: $gp_name, year: $year})
   WHERE ps.milliseconds IS NOT NULL
   RETURN d.forename + ' ' + d.surname AS driver, ps.stop AS stop_number, ps.lap AS lap,
          ps.duration AS duration, ps.milliseconds AS milliseconds, ra.name AS race, p
   ORDER BY ps.milliseconds ASC LIMIT 3
   """)

_t("avg_pit_stops", "pit_stops", ["gp_name", "year"], [],
   "Pit stop data starts in 2011; drivers with zero stops are not in the data, so they are not in the average.",
   """
   MATCH (ps:PitStop)-[:FOR_RACE]->(ra:Race {name: $gp_name, year: $year}), (ps)-[:BY_DRIVER]->(d:Driver)
   WITH ra, d, count(ps) AS stops
   RETURN ra.name AS race, avg(stops) AS avg_stops_per_driver, max(stops) AS max_stops,
          count(d) AS drivers_with_stops
   """)

_t("driver_pit_stops", "pit_stops", ["driver_id", "gp_name", "year"], [],
   "Pit stop data starts in 2011.",
   """
   MATCH p = (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(ps:PitStop)-[:FOR_RACE]->(ra:Race {name: $gp_name, year: $year})
   RETURN d.forename + ' ' + d.surname AS driver, ps.stop AS stop_number, ps.lap AS lap,
          ps.duration AS duration, p
   ORDER BY ps.stop LIMIT 10
   """)

# ===================== 7. season_history =====================
_t("season_points_leaders", "season_history", ["year"], ["top_n"],
   "Sums race points only; sprint points and old best-results rules can differ from the official table.",
   """
   MATCH (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)-[:IN_SEASON]->(:Season {year: $year})
   RETURN d.forename + ' ' + d.surname AS driver, sum(r.points) AS points,
          sum(CASE WHEN r.position = 1 THEN 1 ELSE 0 END) AS wins
   ORDER BY points DESC, wins DESC LIMIT 5
   """)

_t("drivers_in_season", "season_history", ["year"], [],
   "Drivers with at least one race entry that season.",
   """
   MATCH (d:Driver)<-[:BY_DRIVER]-(:Result)-[:FOR_RACE]->(:Race)-[:IN_SEASON]->(:Season {year: $year})
   WITH DISTINCT d
   RETURN count(d) AS drivers, collect(d.surname) AS surnames
   """)

_t("team_changes", "season_history", ["year_a", "year_b"], [],
   "Compares each driver's main team in the two seasons; only drivers who raced in both.",
   """
   MATCH (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race),
         (r)-[:FOR_CONSTRUCTOR]->(c:Constructor)
   WHERE ra.year IN [$year_a, $year_b]
   WITH d, ra.year AS year, c, count(r) AS entries
   ORDER BY entries DESC, c.constructorId ASC
   WITH d, year, collect(c.constructorId)[0] AS primaryId
   WITH d, collect({year: year, cid: primaryId}) AS seasons
   WHERE size(seasons) = 2
   WITH d,
        [s IN seasons WHERE s.year = $year_a][0].cid AS c_a,
        [s IN seasons WHERE s.year = $year_b][0].cid AS c_b
   WHERE c_a <> c_b
   WITH d
   ORDER BY d.surname, d.forename
   RETURN count(d) AS drivers_changed,
          collect(d.forename + ' ' + d.surname) AS drivers
   """)

# ===================== 8. fastest_laps =====================
_t("fastest_lap_of_race", "fastest_laps", ["gp_name", "year"], [],
   "Fastest-lap data starts in 2004.",
   """
   MATCH p = (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race {name: $gp_name, year: $year})
   WHERE r.rank = 1
   RETURN d.forename + ' ' + d.surname AS driver, r.fastestLapTime AS lap_time,
          r.fastestLap AS lap, ra.name AS race, p
   LIMIT 1
   """)

_t("driver_fastest_laps", "fastest_laps", ["driver_id"], ["year_from", "year_to"],
   "Fastest-lap data starts in 2004.",
   """
   MATCH (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)
   WHERE r.rank = 1
     AND ($year_from IS NULL OR ra.year >= $year_from)
     AND ($year_to   IS NULL OR ra.year <= $year_to)
   RETURN d.forename + ' ' + d.surname AS driver, count(r) AS fastest_laps
   """)

_t("fastest_lap_at_circuit", "fastest_laps", ["circuit_id"], [],
   "Fastest-lap data starts in 2004; times are compared as text (M:SS.mmm), so this is the fastest recorded race lap in the data.",
   """
   MATCH (d:Driver)<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)-[:AT_CIRCUIT]->(c:Circuit {circuitId: $circuit_id})
   WHERE r.fastestLapTime IS NOT NULL
   RETURN c.circuit_name AS circuit, d.forename + ' ' + d.surname AS driver,
          r.fastestLapTime AS lap_time, ra.year AS year
   ORDER BY r.fastestLapTime ASC LIMIT 1
   """)

# ===================== prediction-only =====================
_t("driver_recent_form", "podium_prediction", ["driver_id", "before_date"], [],
   "Last five races strictly before the scored race.",
   """
   MATCH (d:Driver {driverId: $driver_id})<-[:BY_DRIVER]-(r:Result)-[:FOR_RACE]->(ra:Race)
   WHERE ra.date < date($before_date)
   WITH d, r, ra
   ORDER BY ra.date DESC LIMIT 5
   RETURN d.forename + ' ' + d.surname AS driver, count(r) AS races_considered,
          avg(r.positionOrder) AS avg_finish, sum(r.points) AS points,
          sum(CASE WHEN r.position <= 3 THEN 1 ELSE 0 END) AS podiums
   """)