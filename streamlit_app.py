import streamlit as st
import requests
from threading import Thread
from flask import Flask, request, jsonify
from analyzer import run_all_scans, load_scan_history
import matplotlib.pyplot as plt
import time
import json

st.set_page_config(page_title="Digital Footprint Analyzer", page_icon="🕵️‍♂️", layout="wide")

# -------------------------
# Flask API
# -------------------------
app = Flask(__name__)

@app.route("/scan", methods=["GET"])
def scan():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter missing"}), 400
    result = run_all_scans(query)
    return jsonify(result)

def run_flask():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

# Run Flask in background
flask_thread = Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
time.sleep(1)

# -------------------------
# Streamlit GUI
# -------------------------
st.title("🕵️‍♂️ Digital Footprint & Privacy Analyzer")

tabs = st.tabs(["Scan", "History"])

# -------------------------
# Scan Tab
# -------------------------
with tabs[0]:
    query = st.text_input("Enter Email / Phone / Username:")

    if st.button("Scan"):
        if not query:
            st.warning("Please enter a valid query!")
        else:
            with st.spinner("Scanning..."):
                try:
                    url = f"http://127.0.0.1:5000/scan?query={query}"
                    response = requests.get(url, timeout=20)
                    try:
                        result = response.json()
                    except ValueError:
                        st.error("API returned invalid JSON.")
                        result = {}

                    if not isinstance(result, dict):
                        st.error("API returned unexpected data format.")
                        result = {}

                    # -------------------------
                    # Display results
                    # -------------------------
                    if result:
                        if "error" in result:
                            st.error(result["error"])

                        if "risk_score" in result:
                            st.subheader("⚠️ Risk Score")
                            st.progress(result["risk_score"])

                        if "email_scan" in result:
                            st.subheader("📧 Email Validation")
                            st.json(result["email_scan"])

                        if "phone_scan" in result:
                            st.subheader("📱 Phone Validation")
                            st.json(result["phone_scan"])

                        if "google_results" in result:
                            st.subheader("🔎 Google Search Results")
                            for url in result["google_results"]:
                                st.write(f"- {url}")

                        if "possible_leaks" in result:
                            st.subheader("💀 Possible Leaks / Exposures")
                            for leak in result["possible_leaks"]:
                                st.write(f"- {leak}")

                        if "recommendation" in result:
                            st.subheader("💡 Recommendations")
                            st.write(result["recommendation"])

                        # -------------------------
                        # Graph Risk Score
                        # -------------------------
                        fig, ax = plt.subplots()
                        ax.bar([result["query"]], [result["risk_score"]], color='red')
                        ax.set_ylim(0, 100)
                        ax.set_ylabel("Risk Score")
                        st.pyplot(fig)

                except requests.exceptions.RequestException as e:
                    st.error(f"Failed to connect to API.\n{e}")

# -------------------------
# History Tab
# -------------------------
with tabs[1]:
    st.subheader("📜 Scan History")
    history = load_scan_history()
    if history:
        for item in reversed(history[-10:]):  # show last 10 scans
            st.markdown(f"**{item['timestamp']} - {item['query']}**")
            st.write(f"Risk Score: {item['risk_score']}")
            st.write(f"Possible Leaks: {', '.join(item['possible_leaks'])}")
    else:
        st.info("No scan history found.")
