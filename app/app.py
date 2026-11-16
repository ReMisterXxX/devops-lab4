import os

from flask import Flask, jsonify, request

import db

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_ENV = os.getenv("APP_ENV", "local")


@app.get("/")
def index():
    return jsonify({"app": "lab4-task-api", "version": APP_VERSION, "environment": APP_ENV})


@app.get("/health")
def health():
    try:
        db.check_db()
        return jsonify({"status": "ok", "database": "connected"})
    except Exception:
        return jsonify({"status": "error", "database": "unavailable"}), 503


@app.get("/tasks")
def get_tasks():
    return jsonify(db.list_tasks())


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify({"error": "Pole 'title' jest wymagane"}), 400
    return jsonify(db.add_task(title)), 201


if __name__ == "__main__":
    db.init_db()
    app.run(host="0.0.0.0", port=5000)
