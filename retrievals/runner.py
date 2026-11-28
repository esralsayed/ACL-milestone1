# retrievals/runner.py
# Runs one Cypher template against Neo4j and returns everything the rest of the app needs.

import os
from neo4j import GraphDatabase
from neo4j.graph import Path, Node, Relationship

from retrievals.templates import TEMPLATES

# config.txt sits in the repo root, one folder above retrievals/
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_driver = None  # created once, reused for every call


def _read_config(filename="config.txt"):
    config = {}
    with open(os.path.join(ROOT, filename), "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "" or "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


def get_driver():
    global _driver
    if _driver is None:
        cfg = _read_config()
        _driver = GraphDatabase.driver(cfg["URI"], auth=(cfg["USERNAME"], cfg["PASSWORD"]))
    return _driver


def _node_id(node):
    # newer neo4j versions use element_id, older ones use id
    return getattr(node, "element_id", None) or node.id


def _clean_value(val):
    # dates and times become plain text so the rows are easy to show and log
    if hasattr(val, "iso_format"):
        return val.iso_format()
    return val


def run_template(name, params):
    """
    name   : a key of TEMPLATES, e.g. "driver_season_stats"
    params : dict of entities, e.g. {"driver_id": 1, "year": 2020}

    Returns a dict with:
      rows, empty, cypher, params, nodes, edges, scope
    or {"error": "..."} if the template name or a required parameter is wrong.
    """
    if name not in TEMPLATES:
        return {"error": "unknown template: " + str(name)}

    t = TEMPLATES[name]

    # 1. every required parameter must be present
    missing = [p for p in t["required"] if params.get(p) is None]
    if missing:
        return {"error": "missing " + ", ".join(missing)}

    # 2. every $param in the query must exist, so optional ones default to None
    full = {k: None for k in t["required"] + t["optional"]}
    for k, v in params.items():
        if k in full:
            full[k] = v

    # 3. run the query
    rows = []
    nodes = {}   # id -> node info (a dict avoids duplicates)
    edges = []

    with get_driver().session() as session:
        result = session.run(t["cypher"], full)
        for record in result:
            row = {}
            for key, val in record.items():
                if isinstance(val, Path):
                    for n in val.nodes:
                        nodes[_node_id(n)] = {
                            "id": _node_id(n),
                            "labels": list(n.labels),
                            **{k: _clean_value(v) for k, v in dict(n).items()},
                        }
                    for rel in val.relationships:
                        edges.append({
                            "start": _node_id(rel.start_node),
                            "type": rel.type,
                            "end": _node_id(rel.end_node),
                        })
                elif isinstance(val, (Node, Relationship)):
                    pass  # not used by our templates
                else:
                    row[key] = _clean_value(val)
            rows.append(row)

    # remove repeated edges (several rows can share the same relationship)
    unique_edges = [dict(t_) for t_ in {tuple(e.items()) for e in edges}]

    return {
        "rows": rows,
        "empty": len(rows) == 0,
        "cypher": t["cypher"],
        "params": full,
        "nodes": list(nodes.values()),
        "edges": unique_edges,
        "scope": t["scope"],
    }


def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None