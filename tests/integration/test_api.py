import os

import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")


def test_health_with_real_database():
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_task_is_saved_in_database():
    created = requests.post(f"{BASE_URL}/tasks", json={"title": "Test integracyjny"}, timeout=5)
    assert created.status_code == 201
    task_id = created.json()["id"]
    tasks = requests.get(f"{BASE_URL}/tasks", timeout=5).json()
    assert any(t["id"] == task_id for t in tasks)
