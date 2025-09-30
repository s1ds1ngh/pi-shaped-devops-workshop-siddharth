from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# intentionally insecure: hardcoded secret (for the assignment)
API_KEY = "SUPERSECRET_HARDCODED_API_KEY"

@app.route("/")
def index():
    return "Vulnerable sample app. Try /health and /secret"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/secret")
def secret():
    # insecure: checks a hardcoded API key in query parameter
    key = request.args.get("key", "")
    if key == API_KEY:
        return jsonify({"secret": "this-is-a-top-secret-data"})
    return jsonify({"error": "invalid key"}), 401

if __name__ == "__main__":
    # run in non-debug mode here; but still insecure due to hardcoded secret + other possible issues
    app.run(host="0.0.0.0", port=5000)
