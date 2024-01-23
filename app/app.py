from flask import Flask
from app.models.task import Task
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db
from .view.task_view import tasks_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:wp@localhost:8083/taskmanagementdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(tasks_blueprint)

if __name__ == "__main__":
    app.run(debug=True)