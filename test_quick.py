# test_quick.py  -  throwaway script to check that the templates work.
# Run from the repo root:  python test_quick.py

from retrievals.runner import run_template, close_driver


def show(title, name, params):
    print("=" * 60)
    print(title)
    r = run_template(name, params)
    if "error" in r:
        print("ERROR:", r["error"])
        return
    print("empty:", r["empty"])
    for row in r["rows"]:
        print(row)
    if r["nodes"]:
        print(len(r["nodes"]), "nodes,", len(r["edges"]), "edges")


# 1. Hamilton 2020 season (driver_id 1)
show("Hamilton 2020", "driver_season_stats", {"driver_id": 1, "year": 2020})

# 2. Podium of a race (graphical: also returns nodes and edges)
show("German GP 2019 podium", "race_podium", {"gp_name": "German Grand Prix", "year": 2019})

# 3. Missing a required parameter -> should print an error, not crash
show("Missing year", "driver_season_stats", {"driver_id": 1})

# 4. A query that should return nothing -> empty should be True
show("Empty result", "driver_season_stats", {"driver_id": 1, "year": 1900})

# 5. Driver at a circuit, before a date (use your own circuit id from Neo4j)
show("Hamilton at circuit 9 before 2020", "driver_at_circuit",
     {"driver_id": 1, "circuit_id": 9, "before_date": "2020-01-01"})

close_driver()