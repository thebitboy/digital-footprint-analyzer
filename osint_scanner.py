import random
from datetime import datetime

def scan_digital_footprint(query):
    """
    Simulates a digital footprint scan using OSINT.
    Returns a dictionary with Google results, leaks, email/phone validation, and risk score.
    """

    google_results = [
        f"https://example.com/search?q={query}",
        f"https://socialmedia.com/{query}",
        f"https://pastebin.com/{query}"
    ]

    possible_leaks = [
        "Email found in leaks",
        "Old account publicly accessible",
        "Social media profile detected",
        "Phone number exposed in spam database"
    ]
    exposed_items = random.sample(possible_leaks, 2)

    risk_score = random.randint(30, 90)

    email_scan = {"format_valid": "@" in query} if "@" in query else {}
    phone_scan = {"valid": query.isdigit()} if query.isdigit() else {}

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "query": query,
        "google_results": google_results,
        "possible_leaks": exposed_items,
        "risk_score": risk_score,
        "email_scan": email_scan,
        "phone_scan": phone_scan,
        "recommendation": "Enable 2FA, delete old accounts, and avoid sharing personal data online.",
        "timestamp": timestamp
    }
