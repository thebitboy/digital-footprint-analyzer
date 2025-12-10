from flask import Flask, request, jsonify
from analyzer import run_all_scans

app = Flask(__name__)

@app.route("/scan", methods=["GET"])
def scan():
    query = request.args.get("query")

    if not query:
        return jsonify({"error": "Query parameter missing"}), 400

    result = run_all_scans(query)
    return jsonify(result)

if __name__ == "__main__":
    print("🚀 Digital Footprint API running at http://127.0.0.1:5000/scan?query=example")
    app.run(host="127.0.0.1", port=5000)
