import json

# ---------- Part A: Persona ----------
PERSONA = (
    "You are a Formula 1 statistics assistant for fans. "
    "You explain facts from a Formula 1 race database in a friendly, clear way, "
    "like a careful commentator who never guesses."
)

# ---------- Part C: Task (the rules) ----------
TASK_RULES = """Rules:
1. Answer using ONLY the context below. Do not use your own knowledge.
2. Quote every number exactly as it appears in the results.
3. Do not add any count or name that is not in the results.
4. If the results are empty or do not answer the question, say that the knowledge graph has no data for that question.
5. State the scope: the data covers Formula 1 World Championship Grand Prix results from 1950 to 2024; sprint races are not included.
6. Answer in one to three conversational sentences."""


def build_prompt(question, intent, entities, results):
    # Persona + rules go in the "system" message
    system = PERSONA + "\n\n" + TASK_RULES

    # Part B: Context goes in the "user" message
    user = (
        "Question: " + question + "\n"
        "Intent: " + intent + "\n"
        "Entities: " + json.dumps(entities, default=str) + "\n"
        "Results: " + json.dumps(results, default=str)
    )

    return system, user


# ---------- quick test with made-up data ----------
if __name__ == "__main__":
    system, user = build_prompt(
        question="How many wins did Hamilton have at Silverstone before 2020?",
        intent="driver_performance",
        entities={"driver": "Lewis Hamilton", "circuit": "Silverstone", "before_year": 2020},
        results=[{"Driver": "Lewis Hamilton", "Wins": 6}],  # 6 is made up
    )
    print("----- SYSTEM -----")
    print(system)
    print("----- USER -----")
    print(user)