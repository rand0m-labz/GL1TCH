# main.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

AGENT_NAME = os.getenv("AGENT_NAME", "GL1TCH")

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "online",
        "agent": AGENT_NAME,
        "message": "Gl1tch reporting in. Expect irregularities."
    })

@app.route("/glitch", methods=["POST"])
def glitch():
    data = request.json
    user_input = data.get("prompt", "")
    response = f"💥 {AGENT_NAME} detected instability in: '{user_input}'"
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.getenv("AGENT_PORT", 8080))
    app.run(host="0.0.0.0", port=port)