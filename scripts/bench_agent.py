Этап 0: Skeleton бэнч-агента
- загрузка inputs/models_list.json и inputs/tokens.json
- фиктивная (покажем как сделать позже) фильтрация по price_rub <= 75
- создание пустого графа graph.json и метрик metrics.json
- запись результатов в bench/results/<model_id>/<run_id>/
import json
import os
from datetime import datetime

def load_json(path):
with open(path, "r", encoding="utf-8") as f:
return json.load(f)

def ensure_dir(p):
os.makedirs(p, exist_ok=True)

def main():
base = os.path.expanduser("~/benchmark_1")
models = load_json(os.path.join(base, "bench", "inputs", "models_list.json"))
model_id = models[0]["model_id"] if models else "demo_model"
run_id = "run_" + datetime.now().strftime("%Y%m%d_%H%M%S")
dst = os.path.join(base, "bench", "results", model_id, run_id)
ensure_dir(dst)
graph = {"model_id": model_id, "run_id": run_id, "graph": {"nodes": [], "edges": []}}
metrics = {"latency_ms": 0, "memory_mb": 0, "edge_count": 0, "node_count": 0}
with open(os.path.join(dst, "graph.json"), "w", encoding="utf-8") as f:
json.dump(graph, f, ensure_ascii=False, indent=2)
with open(os.path.join(dst, "metrics.json"), "w", encoding="utf-8") as f:
json.dump(metrics, f, ensure_ascii=False, indent=2)
print(f"Created placeholder results in {dst}")

if name == "main":
main()
