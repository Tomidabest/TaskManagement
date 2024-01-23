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
    """
    Create a Task
    ---
    tags:
      - tasks
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: TaskInput
          required:
            - description
          properties:
            description:
              type: string
              description: Description of the task.
    responses:
      201:
        description: Task created successfully.
        schema:
          id: TaskOutput
          properties:
            id:
              type: integer
              description: Unique identifier of the task.
            description:
              type: string
              description: Description of the task.
            completed:
              type: boolean
              description: Status of the task.
            created_at:
              type: string
              description: Timestamp of task creation.
            updated_at:
              type: string
              description: Timestamp of the last task update.
      400:
        description: Invalid input.
    """
    data = request.get_json()
    description = data.get('description')
    if not description:
        return jsonify({'message': 'Description is required'}), 400
    new_task = create_task_logic(description)
    return jsonify(new_task.to_dict()), 201

@tasks_blueprint.route('/tasks', methods=['GET'])
def get_all_tasks():
    """
    Get all Tasks
    ---
    tags:
      - tasks
    responses:
      200:
        description: An array of tasks
        schema:
          type: array
          items:
            $ref: '#/definitions/TaskOutput'
    """
    tasks = get_all_tasks_logic()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """
    Get a single Task
    ---
    tags:
      - tasks
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: Unique identifier of the task
    responses:
      200:
        description: A single task
        schema:
          $ref: '#/definitions/TaskOutput'
      404:
        description: Task not found
    """
    task = get_task_logic(task_id)
    if task:
        return jsonify(task.to_dict()), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@tasks_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """
    Update a Task
    ---
    tags:
      - tasks
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: Unique identifier of the task
      - in: body
        name: body
        required: true
        schema:
          id: TaskUpdateInput
          properties:
            description:
              type: string
              description: Updated description of the task.
            completed:
              type: boolean
              description: Updated status of the task.
    responses:
      200:
        description: Task updated successfully
        schema:
          $ref: '#/definitions/TaskOutput'
      404:
        description: Task not found
    """
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
    """
    Delete a Task
    ---
    tags:
      - tasks
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: Unique identifier of the task
    responses:
      200:
        description: Task deleted successfully
      404:
        description: Task not found
    """
    task = delete_task_logic(task_id)
    if task:
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'message': 'Task not found'}), 404

@tasks_blueprint.route('/tasks', methods=['DELETE'])
def delete_all_tasks():
    """
    Delete all Tasks
    ---
    tags:
      - tasks
    responses:
      200:
        description: All tasks deleted successfully
    """
    try:
        num_deleted = delete_all_tasks_logic()
        return jsonify({'message': f'All tasks deleted successfully, count: {num_deleted}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500