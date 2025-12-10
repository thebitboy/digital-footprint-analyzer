import json
import os

DB_FILE = "monitor.json"

def save_monitor(target):
    data = load_monitor()
    if target not in data:
        data.append(target)
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def load_monitor():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)
