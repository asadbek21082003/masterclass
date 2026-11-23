import os
import requests
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=None)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

@app.get("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

@app.post("/submit")
def submit():
    d = request.get_json(silent=True) or {}
    name = str(d.get("name", "")).strip()[:100]
    phone = str(d.get("phone", "")).strip()[:30]
    role = str(d.get("role", "")).strip()[:50]
    center = str(d.get("center", "")).strip()[:100] or "-"
    if len(name) < 3 or sum(c.isdigit() for c in phone) < 9:
        return jsonify(ok=False), 400
    text = (
        "Yangi ariza (Masterclass, 1-dekabr)\n"
        f"Ism: {name}\nTelefon: {phone}\nRoli: {role}\nMarkaz: {center}"
    )
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=10,
        )
        r.raise_for_status()
    except Exception:
        return jsonify(ok=False), 502
    return jsonify(ok=True)