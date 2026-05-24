#!/usr/bin/env python3
import json
import os
import re
import hashlib
from datetime import datetime, timezone
import time
import sys

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def compute_base():
    # Базовый путь — корень проекта Text-to-geniolgy (root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base = os.path.abspath(os.path.join(script_dir, ".."))
    # Если структура отличается и inputs отсутствуют, подстраховка на уровень выше
    if not os.path.exists(os.path.join(base, "inputs")):
        base = os.path.abspath(os.path.join(script_dir, "..", ".."))
    return base

def resolve_input_paths(base):
    bench_inputs = os.path.join(base, "inputs")
    models_list_path = None
    for fname in ("models_list.json", "models-list.json"):
        p = os.path.join(bench_inputs, fname)
        if os.path.exists(p):
            models_list_path = p
            break

    test_text_path = None
    for fname in ("test_text.txt", "test_text.json", "text_test.json", "text_test.txt"):
        p = os.path.join(bench_inputs, fname)
        if os.path.exists(p):
            test_text_path = p
            break

    return models_list_path, test_text_path

# Простая система узла-идентификаторов
def extract_graph_from_text(text):
    nodes = {}
    edges = []

    def add_node(name):
        key = name.strip()
        if key not in nodes:
            nodes[key] = name.strip()
        return key

    # 1) "X был(а) сыном Y и Z"
    m = re.search(r"([А-ЯЁ][а-яё]+) был(?:а|) сыном ([^.;,]+?)(?:\.|,|;)", text)
    if m:
        child = m.group(1)
        parents_str = m.group(2)
        child_id = add_node(child)
        for p in re.split(r"\s+и\s+|,|;", parents_str):
            p = p.strip()
            if not p:
                continue
            pid = add_node(p)
            edges.append({"from": pid, "to": child_id, "relation": "parent_of"})

    # 2) "X был(а) дочерью Y"
    m = re.search(r"([А-ЯЁ][а-яё]+) был(?:а|) дочерью ([^.;,]+?)(?:\.|,|;)", text)
    if m:
        child = m.group(1)
        parents_str = m.group(2)
        child_id = add_node(child)
        for p in re.split(r"\s+и\s+|,|;", parents_str):
            p = p.strip()
            if not p:
                continue
            pid = add_node(p)
            edges.append({"from": pid, "to": child_id, "relation": "parent_of"})

    # 3) "X был(а) дядя Y" / "брат Z" -> сопутствующая обработка
    m = re.search(r"([А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)?)\s*был(?:а|) дядя ([^.;,]+)", text)
    if m:
        uncle = m.group(1)
        rest = m.group(2)
        m2 = re.search(r"брат\s+([А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)?)", rest)
        if m2:
            brother = m2.group(1)
            uid = add_node(uncle)
            bid = add_node(brother)
            edges.append({"from": uid, "to": bid, "relation": "sibling_of"})
            edges.append({"from": bid, "to": uid, "relation": "sibling_of"})

    # 4) "X женат на Y" / "X замужем на Y" -> spouse_of
    m = re.search(r"([А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+)*)\s+(?:женат на|замужем на)\s+([^.;,]+)", text)
    if m:
        a = add_node(m.group(1))
        bname = m.group(2).strip()
        b = add_node(bname)
        edges.append({"from": a, "to": b, "relation": "spouse_of"})
        edges.append({"from": b, "to": a, "relation": "spouse_of"})

    # 5) "У X есть дед Y" / бабушка — простая подпись
    m = re.search(r"У\s+([А-ЯЁ][а-яё]+(?: [А-ЯЁ][а-яё]+){0,2})\s+есть дед\s+([^.;,]+)", text)
    if m:
        parent = m.group(1)
        gp = m.group(2).strip()
        pid = add_node(parent)
        gpid = add_node(gp)
        edges.append({"from": gpid, "to": pid, "relation": "parent_of"})

    return {"nodes": [{"id": k, "name": v} for k, v in nodes.items()], "edges": edges}

def compute_digest(text):
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    words = len(text.split())
    chars = len(text)
    return {"sha256": sha, "word_count": words, "char_count": chars}

def main():
    base = compute_base()
    models_list_path, test_text_path = resolve_input_paths(base)

    models = []
    if models_list_path:
        try:
            models = load_json(models_list_path)
        except Exception:
            models = []

    text = ""
    if test_text_path:
        if test_text_path.endswith(".json"):
            try:
                data = load_json(test_text_path)
                if isinstance(data, dict):
                    text = data.get("text", "")
                elif isinstance(data, str):
                    text = data
            except Exception:
                text = ""
        else:
            text = load_text(test_text_path)

    # Выбор модели
    model_id = "demo_model"
    if models:
        if isinstance(models, dict) and "default_model" in models:
            model_id = str(models.get("default_model", model_id))
        elif isinstance(models, list) and len(models) > 0 and isinstance(models[0], dict):
            model_id = str(models[0].get("model_id", model_id))

    run_id = "run_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(base, "results", model_id, run_id)
    ensure_dir(dst)

    graph_struct = extract_graph_from_text(text)
    graph = {"model_id": model_id, "run_id": run_id, "graph": graph_struct}
    node_count = len(graph_struct.get("nodes", []))
    edge_count = len(graph_struct.get("edges", []))

    metrics = {
        "latency_ms": 0,
        "memory_mb": 0,
        "edge_count": edge_count,
        "node_count": node_count
    }

    with open(os.path.join(dst, "graph.json"), "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)

    with open(os.path.join(dst, "metrics.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

    digest = compute_digest(text)
    with open(os.path.join(dst, "input_digest.json"), "w", encoding="utf-8") as f:
        json.dump(digest, f, ensure_ascii=False, indent=2)

    metadata = {
        "model_id": model_id,
        "run_id": run_id,
        "start_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "end_time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model_meta": models,
        "input_summary": {
            "text_digest": digest["sha256"],
            "text_length_words": digest["word_count"]
        }
    }
    with open(os.path.join(dst, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    logs_dir = os.path.join(base, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, run_id + ".log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Benchmark Stage 0 completed. run_id={run_id}\n")
        f.write(f"Model: {model_id}, Persons: {node_count}, Edges: {edge_count}\n")

    print(f"Benchmark Stage 0 completed. Results written to {dst}")

if __name__ == "__main__":
    sys.exit(main())
