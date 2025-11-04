# main.py
from flask import Flask, request, jsonify
import os, requests

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
    prompt = data.get("prompt", "")
    n8n_url = os.getenv("WEBHOOK_URL", "http://localhost:5678/webhook-test/gl1tch-test")

    try:
        # prompt --> n8n webhook
        r = requests.post(n8n_url, json={"prompt": prompt}, timeout=10)
        n8n_response = r.json()
    except Exception as e:
        # connection failure --> fallback to local response
        n8n_response = {"reply": f"⚠️ N8N connection failed: {e}"}

    return jsonify({
        "reply": n8n_response.get("reply", f"💥 {AGENT_NAME} detected instability in: '{prompt}'")
    })