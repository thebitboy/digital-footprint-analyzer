from osint_scanner import scan_digital_footprint
import json
import os

HISTORY_FILE = "scan_history.json"

def run_all_scans(query):
    """
    Runs OSINT scan and saves history.
    """
    try:
        result = scan_digital_footprint(query)
        if not isinstance(result, dict):
            result = {}
    except Exception as e:
        result = {"error": f"Scanner failed: {e}"}

    # Ensure default keys exist
    defaults = {
        "query": query,
        "google_results": [],
        "possible_leaks": [],
        "risk_score": 0,
        "email_scan": {},
        "phone_scan": {},
        "recommendation": "",
        "timestamp": ""
    }
    defaults.update(result)

    # Save to history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append(defaults)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    return defaults

def load_scan_history():
    """
    Loads scan history from JSON file.
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []
