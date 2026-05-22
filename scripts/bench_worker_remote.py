Каркас удаленного инференса (пока заглушка)
import sys, json

def main():
# В реальном прогоне примем параметры, вызов инференса и вернем graph.json + metrics.json
out = {"graph": {"nodes": [], "edges": []}, "metrics": {"latency_ms": 0, "memory_mb": 0}}
print(json.dumps(out))

if name == "main":
main()

2.7. Файл: bench/logs/bench_run.log
[INFO] Run placeholder created
[INFO] bench/scripts/bench_agent.py completed

2.8. Файл: bench/results/tiny-ru-en-translate-01/run_20260522_120000/graph.json
{
"model_id": "tiny-ru-en-translate-01",
"run_id": "run_20260522_120000",
"graph": {
"nodes": [
{"id": "Иван_Петрович", "name": "Иван Петрович"},
{"id": "Алексей", "name": "Алексей"},
{"id": "Мария", "name": "Мария"},
{"id": "Наталья", "name": "Наталья"},
{"id": "Ксения", "name": "Ксения"}
],
"edges": [
{"source": "Иван_Петрович", "target": "Алексей", "relation": "parent_of"},
{"source": "Иван_Петрович", "target": "Мария", "relation": "parent_of"},
{"source": "Наталья", "target": "Алексей", "relation": "spouse_of"},
{"source": "Алексей", "target": "Ксения", "relation": "parent_of"},
{"source": "Наталья", "target": "Ксения", "relation": "parent_of"}
]
},
"input_digest": "sha256:abcdef1234567890",
"notes": "translation_support: true, languages: [ru,en]"
}

2.9. Файл: bench/results/tiny-ru-en-translate-01/run_20260522_120000/metrics.json
{
"latency_ms": 1000,
"memory_mb": 256,
"edge_count": 5,
"node_count": 5,
"precision": null,
"recall": null,
"f1": null
}

2.10. Файл: bench/results/tiny-ru-en-translate-01/run_20260522_120000/input_digest.json
{
"sha256": "abcdef1234567890",
"word_count": 69,
"char_count": 420
}

2.11. Файл: bench/results/tiny-ru-en-translate-01/run_20260522_120000/metadata.json
{
"model_id": "tiny-ru-en-translate-01",
"run_id": "run_20260522_120000",
"start_time": "2026-05-22T12:00:00Z",
"end_time": "2026-05-22T12:00:02Z",
"model_meta": {
"provider": "Local-LM",
"size_mb": 50,
"quantization": "int8",
"price_rub": 60,
"languages": ["ru","en"]
},
"input_summary": {
"text_digest": "abcdef1234",
"text_length_words": 69
}
}

2.12. Файл: bench/results/tiny-ru-en-translate-01/run_20260522_120000/logs/stdout.log
[INFO] Run 20260522_120000 started
[INFO] Graph generated with 5 nodes and 5 edges
[INFO] Metrics computed: latency 1000 ms, memory 256 MB

Текстовая инструкция по запуску (коротко)
Перейдите в каталог ~/benchmark_1.
Убедитесь, что структура соответствует приведенной выше.
Запустите минимальный прогон:
python3 bench/scripts/bench_agent.py
После выполнения будут созданы каталоги bench/results/tiny-ru-en-translate-01/run_YYYYMMDD_HHMMSS с graph.json и metrics.json и сопутствующими файлами.
Посмотрите сводку (если хотите) в bench/benchmark_report.json (пусто до прогонов; можно заполнить позже).
Примечания
Все токены и реальные ссылки замените на свои. Вготовых примерах используются заглушки.
Этот каркас предназначен для быстрого старта. По мере роста можно заменить заглушки на реальную логику инференса (удаленно через API/туннель или локально через llama.cpp и т.д.).
Если нужно, могу подготовить пакет архива (zip/tar) с этими же файлами и готовым архивом, чтобы просто разархивировать и начать работу.
Сообщите, пожалуйста:

Подтверждаете ли вы этот чистый старт?
Или хотите сразу получить готовый архив (zip) с этими файлами и инструкциями?
tunnel (gpt-5-nano)

· 32474 tokens






















Введите ваш вопрос здесь...



2K

T
gpt-5-nano

Контент, сгенерированный AI, может быть неточным. Пожалуйста, проверяйте важную информа
