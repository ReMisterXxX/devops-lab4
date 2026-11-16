import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "app"))

import app as application  # noqa: E402


@pytest.fixture
def client(monkeypatch):
    tasks = []

    def fake_add(title):
        task = {"id": len(tasks) + 1, "title": title, "done": False}
        tasks.append(task)
        return task

    monkeypatch.setattr(application.db, "list_tasks", lambda: tasks)
    monkeypatch.setattr(application.db, "add_task", fake_add)
    monkeypatch.setattr(application.db, "check_db", lambda: True)
    return application.app.test_client()


def test_index_returns_version(client):
    data = client.get("/").get_json()
    assert data["app"] == "lab4-task-api"
    assert "version" in data


def test_health_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_create_and_list_tasks(client):
    response = client.post("/tasks", json={"title": "Napisac sprawozdanie"})
    assert response.status_code == 201
    assert client.get("/tasks").get_json()[0]["title"] == "Napisac sprawozdanie"


def test_create_task_without_title(client):
    assert client.post("/tasks", json={}).status_code == 400


def test_health_when_db_down(client, monkeypatch):
    def broken():
        raise ConnectionError

    monkeypatch.setattr(application.db, "check_db", broken)
    assert client.get("/health").status_code == 503
