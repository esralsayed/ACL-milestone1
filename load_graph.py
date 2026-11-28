import os
import csv
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_config(filename="config.txt"):
    path = os.path.join(BASE_DIR, filename)
    config = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "" or "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


config = read_config()
URI = config["URI"]
USERNAME = config["USERNAME"]
PASSWORD = config["PASSWORD"]

print("Config file read successfully!")


from neo4j import GraphDatabase

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
driver.verify_connectivity()
print("Connected to Neo4j!")


# ---------- Step 3: uniqueness constraints ----------
constraints = [
    ("Driver", "driverId"),
    ("Constructor", "constructorId"),
    ("Circuit", "circuitId"),
    ("Season", "year"),
    ("Status", "statusId"),
    ("Race", "raceId"),
    ("Result", "resultId"),
    ("Qualifying", "qualifyId"),
    ("PitStop", "eventId"),
]

with driver.session() as session:
    for label, prop in constraints:
        session.run(
            f"CREATE CONSTRAINT {label.lower()}_{prop}_unique IF NOT EXISTS "
            f"FOR (n:{label}) REQUIRE n.{prop} IS UNIQUE"
        )

print("Constraints ready.")


# ---------- Step 4: helper functions ----------
def is_missing(value):
    return value is None or value.strip() == "" or value.strip() == "\\N"

def to_int(value):
    if is_missing(value):
        return None
    return int(value.strip())

def to_float(value):
    if is_missing(value):
        return None
    return float(value.strip())

def to_str(value):
    if is_missing(value):
        return None
    return value.strip()

def to_date(value):
    if is_missing(value):
        return None
    return date.fromisoformat(value.strip())

def clean(props):
    return {key: value for key, value in props.items() if value is not None}

def read_csv(filename):
    path = os.path.join(BASE_DIR, "csvs", filename)
    with open(path, "r", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ---------- Step 5: entity nodes ----------
def run_in_batches(query, rows, batch_size=1000):
    with driver.session() as session:
        for start in range(0, len(rows), batch_size):
            session.run(query, rows=rows[start:start + batch_size]).consume()


# ---- Driver ----
drivers = []
for r in read_csv("drivers.csv"):
    drivers.append({
        "id": to_int(r["driverId"]),
        "props": clean({
            "driverId": to_int(r["driverId"]),
            "driverRef": to_str(r["driverRef"]),
            "number": to_int(r["number"]),
            "code": to_str(r["code"]),
            "forename": to_str(r["forename"]),
            "surname": to_str(r["surname"]),
            "dob": to_date(r["dob"]),
            "nationality": to_str(r["nationality"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Driver {driverId: row.id})
    SET n += row.props
""", drivers)
print("Drivers:", len(drivers))


# ---- Constructor ----
constructors = []
for r in read_csv("constructors.csv"):
    constructors.append({
        "id": to_int(r["constructorId"]),
        "props": clean({
            "constructorId": to_int(r["constructorId"]),
            "constructorRef": to_str(r["constructorRef"]),
            "constructor_name": to_str(r["name"]),
            "constructor_nationality": to_str(r["nationality"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Constructor {constructorId: row.id})
    SET n += row.props
""", constructors)
print("Constructors:", len(constructors))


# ---- Circuit ----
circuits = []
for r in read_csv("circuits.csv"):
    circuits.append({
        "id": to_int(r["circuitId"]),
        "props": clean({
            "circuitId": to_int(r["circuitId"]),
            "circuitRef": to_str(r["circuitRef"]),
            "circuit_name": to_str(r["name"]),
            "circuit_loc": to_str(r["location"]),
            "circuit_country": to_str(r["country"]),
            "lat": to_float(r["lat"]),
            "lng": to_float(r["lng"]),
            "alt": to_int(r["alt"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Circuit {circuitId: row.id})
    SET n += row.props
""", circuits)
print("Circuits:", len(circuits))


# ---- Season ----
seasons = []
for r in read_csv("seasons.csv"):
    seasons.append({"id": to_int(r["year"])})
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Season {year: row.id})
""", seasons)
print("Seasons:", len(seasons))


# ---- Status ----
statuses = []
for r in read_csv("status.csv"):
    statuses.append({
        "id": to_int(r["statusId"]),
        "props": clean({
            "statusId": to_int(r["statusId"]),
            "status": to_str(r["status"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Status {statusId: row.id})
    SET n += row.props
""", statuses)
print("Statuses:", len(statuses))


# ---- Race (+ AT_CIRCUIT and IN_SEASON arrows) ----
races = []
for r in read_csv("races.csv"):
    races.append({
        "id": to_int(r["raceId"]),
        "circuitId": to_int(r["circuitId"]),
        "year": to_int(r["year"]),
        "props": clean({
            "raceId": to_int(r["raceId"]),
            "year": to_int(r["year"]),
            "round": to_int(r["round"]),
            "name": to_str(r["name"]),
            "date": to_date(r["date"]),
            "time": to_str(r["time"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Race {raceId: row.id})
    SET n += row.props
    WITH n, row
    MATCH (c:Circuit {circuitId: row.circuitId})
    MATCH (s:Season {year: row.year})
    MERGE (n)-[:AT_CIRCUIT]->(c)
    MERGE (n)-[:IN_SEASON]->(s)
""", races)
print("Races:", len(races))


# ---------- Step 6: fact nodes ----------

# ---- Result (+ 4 arrows) ----
results = []
for r in read_csv("results.csv"):
    results.append({
        "id": to_int(r["resultId"]),
        "raceId": to_int(r["raceId"]),
        "driverId": to_int(r["driverId"]),
        "constructorId": to_int(r["constructorId"]),
        "statusId": to_int(r["statusId"]),
        "props": clean({
            "resultId": to_int(r["resultId"]),
            "number": to_int(r["number"]),
            "grid": to_int(r["grid"]),
            "position": to_int(r["position"]),
            "positionText": to_str(r["positionText"]),
            "positionOrder": to_int(r["positionOrder"]),
            "points": to_float(r["points"]),
            "laps": to_int(r["laps"]),
            "time": to_str(r["time"]),
            "milliseconds": to_int(r["milliseconds"]),
            "fastestLap": to_int(r["fastestLap"]),
            "rank": to_int(r["rank"]),
            "fastestLapTime": to_str(r["fastestLapTime"]),
            "fastestLapSpeed": to_float(r["fastestLapSpeed"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Result {resultId: row.id})
    SET n += row.props
    WITH n, row
    MATCH (ra:Race {raceId: row.raceId})
    MATCH (d:Driver {driverId: row.driverId})
    MATCH (c:Constructor {constructorId: row.constructorId})
    MATCH (s:Status {statusId: row.statusId})
    MERGE (n)-[:FOR_RACE]->(ra)
    MERGE (n)-[:BY_DRIVER]->(d)
    MERGE (n)-[:FOR_CONSTRUCTOR]->(c)
    MERGE (n)-[:HAS_STATUS]->(s)
""", results)
print("Results:", len(results))


# ---- Qualifying (+ 3 arrows) ----
qualifying = []
for r in read_csv("qualifying.csv"):
    qualifying.append({
        "id": to_int(r["qualifyId"]),
        "raceId": to_int(r["raceId"]),
        "driverId": to_int(r["driverId"]),
        "constructorId": to_int(r["constructorId"]),
        "props": clean({
            "qualifyId": to_int(r["qualifyId"]),
            "number": to_int(r["number"]),
            "position": to_int(r["position"]),
            "q1": to_str(r["q1"]),
            "q2": to_str(r["q2"]),
            "q3": to_str(r["q3"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:Qualifying {qualifyId: row.id})
    SET n += row.props
    WITH n, row
    MATCH (ra:Race {raceId: row.raceId})
    MATCH (d:Driver {driverId: row.driverId})
    MATCH (c:Constructor {constructorId: row.constructorId})
    MERGE (n)-[:FOR_RACE]->(ra)
    MERGE (n)-[:BY_DRIVER]->(d)
    MERGE (n)-[:FOR_CONSTRUCTOR]->(c)
""", qualifying)
print("Qualifying:", len(qualifying))


# ---- PitStop (+ 2 arrows) ----
pit_stops = []
for r in read_csv("pit_stops.csv"):
    race_id = to_int(r["raceId"])
    driver_id = to_int(r["driverId"])
    stop = to_int(r["stop"])
    event_id = f"{race_id}:{driver_id}:{stop}"
    pit_stops.append({
        "id": event_id,
        "raceId": race_id,
        "driverId": driver_id,
        "props": clean({
            "eventId": event_id,
            "stop": stop,
            "lap": to_int(r["lap"]),
            "time": to_str(r["time"]),
            "duration": to_str(r["duration"]),
            "milliseconds": to_int(r["milliseconds"]),
        }),
    })
run_in_batches("""
    UNWIND $rows AS row
    MERGE (n:PitStop {eventId: row.id})
    SET n += row.props
    WITH n, row
    MATCH (ra:Race {raceId: row.raceId})
    MATCH (d:Driver {driverId: row.driverId})
    MERGE (n)-[:FOR_RACE]->(ra)
    MERGE (n)-[:BY_DRIVER]->(d)
""", pit_stops)
print("PitStops:", len(pit_stops))


driver.close()
print("Done.")