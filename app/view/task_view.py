from flask import Blueprint, request, jsonify
from app.controller.task_controller import (
    create_task_logic, 
    get_task_logic, 
    get_all_tasks_logic, 
    update_task_logic, 
    delete_task_logic, 
    delete_all_tasks_logic
)

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'message': 'Description is required'}), 400
    new_task = create_task_logic(description)
    return jsonify(new_task.to_dict()), 201

@tasks_blueprint.route('/tasks', methods=['GET'])
def get_all_tasks():
    tasks = get_all_tasks_logic()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = get_task_logic(task_id)
    if task:
        return jsonify(task.to_dict()), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    description = data.get('description')
    completed = data.get('completed', False)
    task = update_task_logic(task_id, description, completed)
    if task:
        return jsonify(task.to_dict()), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = delete_task_logic(task_id)
    if task:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@tasks_blueprint.route('/tasks', methods=['DELETE'])
def delete_all_tasks():
    try:
        num_deleted = delete_all_tasks_logic()
        return jsonify({'message': f'All tasks deleted successfully, count: {num_deleted}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500