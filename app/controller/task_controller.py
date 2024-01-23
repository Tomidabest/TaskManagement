from app.models.task import Task
from app.app import db

def create_task_logic(description):
    new_task = Task(description=description)
    db.session.add(new_task)
    db.session.commit()
    return new_task

def get_task_logic(task_id):
    return Task.query.get(task_id)

def get_all_tasks_logic():
    return Task.query.all()

def update_task_logic(task_id, description, completed):
    task = Task.query.get(task_id)
    if task:
        task.description = description
        task.completed = completed
        db.session.commit()
        return task
    return None

def delete_task_logic(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return task
    return None

def delete_all_tasks_logic():
    try:
        num_deleted = Task.query.delete()
        db.session.commit()
        return num_deleted
    except Exception as e:
        db.session.rollback()
        return str(e)