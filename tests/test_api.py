import pytest
import json
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["app"] == "devops-task-api"

def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "tasks" in data
    assert len(data["tasks"]) >= 2

def test_create_task(client):
    response = client.post('/tasks', json={"title": "Test Task"})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["task"]["title"] == "Test Task"

def test_create_task_missing_title(client):
    response = client.post('/tasks', json={"completed": True})
    assert response.status_code == 400

def test_metrics(client):
    # Make a request to generate some metrics
    client.get('/health')
    response = client.get('/metrics')
    assert response.status_code == 200
    # Ensure our custom metrics exist in the output
    assert b"app_request_count" in response.data
