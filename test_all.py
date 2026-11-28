# test_all.py - runs every template once with sample inputs.
# Run from the repo root:  python test_all.py
from retrievals.runner import run_template, get_driver, close_driver


def find(query, **params):
    with get_driver().session() as s:
        rec = s.run(query, params).single()
        return rec[0] if rec else None


def drv(forename, surname):
    return find("MATCH (d:Driver {forename:$f, surname:$s}) RETURN d.driverId LIMIT 1", f=forename, s=surname)

def con(name):
    return find("MATCH (c:Constructor {constructor_name:$n}) RETURN c.constructorId LIMIT 1", n=name)

def cir(loc):
    return find("MATCH (c:Circuit) WHERE c.circuit_loc = $l RETURN c.circuitId LIMIT 1", l=loc)


ham, nor, ric, ver = drv("Lewis", "Hamilton"), drv("Lando", "Norris"), drv("Daniel", "Ricciardo"), drv("Max", "Verstappen")
mer, mcl, wil = con("Mercedes"), con("McLaren"), con("Williams")
silverstone, monza = cir("Silverstone"), cir("Monza")

print("IDs:", dict(ham=ham, nor=nor, ric=ric, ver=ver, mer=mer, mcl=mcl, wil=wil, silverstone=silverstone, monza=monza))

CASES = [
    ("driver_season_stats",    {"driver_id": ham, "year": 2020}),
    ("driver_totals",          {"driver_id": ham, "year_from": 2014, "year_to": 2020}),
    ("driver_at_circuit",      {"driver_id": ham, "circuit_id": silverstone, "before_date": "2020-01-01"}),
    ("constructor_totals",     {"constructor_id": mer, "year_from": 2014, "year_to": 2020}),
    ("constructor_reliability",{"constructor_id": wil, "year_from": 2014, "year_to": 2021}),
    ("constructor_drivers",    {"constructor_id": mcl, "year": 2019}),
    ("teammate_race_h2h",      {"driver_a_id": nor, "driver_b_id": ric, "year_from": 2021, "year_to": 2022}),
    ("teammate_quali_h2h",     {"driver_a_id": nor, "driver_b_id": ric, "year_from": 2021, "year_to": 2022}),
    ("race_podium",            {"gp_name": "German Grand Prix", "year": 2019}),
    ("circuit_info",           {"circuit_id": silverstone}),
    ("top_winners_at_circuit", {"circuit_id": silverstone}),
    ("pole_sitter",            {"gp_name": "Monaco Grand Prix", "year": 2019}),
    ("driver_poles",           {"driver_id": ham}),
    ("grid_gains",             {"circuit_id": monza, "year": 2021}),
    ("fastest_pit_stops",      {"gp_name": "Qatar Grand Prix", "year": 2023}),
    ("avg_pit_stops",          {"gp_name": "Qatar Grand Prix", "year": 2023}),
    ("driver_pit_stops",       {"driver_id": ver, "gp_name": "Qatar Grand Prix", "year": 2023}),
    ("season_points_leaders",  {"year": 2021}),
    ("drivers_in_season",      {"year": 2021}),
    ("team_changes",           {"year_a": 2020, "year_b": 2021}),
    ("fastest_lap_of_race",    {"gp_name": "Italian Grand Prix", "year": 2021}),
    ("driver_fastest_laps",    {"driver_id": ham}),
    ("fastest_lap_at_circuit", {"circuit_id": silverstone}),
    ("driver_recent_form",     {"driver_id": ham, "before_date": "2021-03-28"}),
]

for name, params in CASES:
    r = run_template(name, params)
    if "error" in r:
        print(f"[ERROR] {name}: {r['error']}")
    elif r["empty"]:
        print(f"[EMPTY] {name}  params={params}")
    else:
        print(f"[ok]    {name}: {len(r['rows'])} row(s), first = {r['rows'][0]}")

close_driver()