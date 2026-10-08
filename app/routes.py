from flask import Blueprint, jsonify, request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

bp = Blueprint('main', __name__)

# In-memory storage for tasks
tasks = [
    {"id": 1, "title": "Setup Git", "completed": True},
    {"id": 2, "title": "Write Dockerfile", "completed": False}
]

@bp.route('/', methods=['GET'])
def index():
    return jsonify({
        "app": "devops-task-api",
        "version": "1.0",
        "description": "Simple API for DevOps CIE demonstration"
    })

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    if 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_task = {
        "id": len(tasks) + 1,
        "title": data['title'],
        "completed": data.get('completed', False)
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201

@bp.route('/metrics', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
