import sys, json

def main():
# В реальном прогоне здесь будет вызов API/туннеля и возврат graph.json + metrics.json
out = {"graph": {"nodes": [], "edges": []}, "metrics": {"latency_ms": 0, "memory_mb": 0}}
print(json.dumps(out))

if name == "main":
main()
