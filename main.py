import json
import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Basic app configuration
app = Flask(__name__)
API_KEY = "TopSecretAPIKEY"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class ToDoTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    responsible = db.Column(db.String(250), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    duedate = db.Column(db.DateTime, nullable=True)
    done = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route('/todos', methods=['GET'])
def get_all_tasks():
    todos = db.session.query(ToDoTask).all()
    todos_json = [task.to_dict() for task in todos]
    return jsonify(todos=todos_json)


@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = db.session.query(ToDoTask).where(ToDoTask.id == todo_id).first()
    if todo:
        return jsonify(todotask=todo.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, a todo with that id does not exist in the database"}), 404


@app.route('/todos', methods=['POST'])
def add_todo():
    body = request.get_json()
    if request.args.get('api-key') == API_KEY:
        body_dict = json.loads(body)
        new_todo = ToDoTask(
            description=body_dict.get('description'),
            responsible=body_dict.get('responsible'),
            created=datetime.strptime(body_dict.get('created'), '%Y-%m-%d %H:%M:%S.%f'),
            duedate=datetime.strptime(body_dict.get('duedate'), '%Y-%m-%d %H:%M:%S.%f'),
            done=body_dict.get('done'),
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({"success": "Successfully removed the todo."}), 200
    else:
        return jsonify(error={"Not Allowed": "Sorry, the key provided is not correct"}), 403

@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    body = request.get_json()
    todo = db.session.query(ToDoTask).where(ToDoTask.id == todo_id).first()
    if todo:
        if request.args.get('api-key') == API_KEY:
            new_todo = json.loads(body)
            todo.description = new_todo.get('description')
            todo.responsible = new_todo.get('responsible')
            todo.done = new_todo.get('done')
            todo.duedate = datetime.strptime(new_todo.get('duedate'), '%Y-%m-%d %H:%M:%S.%f')
            db.session.commit()
            return jsonify({"success": "Successfully removed the todo."}), 200
        else:
            return jsonify(error={"Not Allowed": "Sorry, the key provided is not correct"}), 403
    else:
        return jsonify(error={"Not Found": "Sorry, a todo with that id does not exist in the database"}), 404


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = db.session.query(ToDoTask).where(ToDoTask.id == todo_id).first()
    if todo:
        if request.args.get('api-key') == API_KEY:
            db.session.delete(todo)
            db.session.commit()
            return jsonify({"success": "Successfully removed the todo."}), 200
        else:
            return jsonify(error={"Not Allowed": "Sorry, the key provided is not correct"}), 403
    else:
        return jsonify(error={"Not Found": "Sorry, a todo with that id does not exist in the database"}), 404


if __name__ == '__main__':
    app.run(debug=True)
