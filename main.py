import os
from datetime import datetime

from flask import Flask, jsonify
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
    created = db.Column(db.DateTime, default=datetime.utcnow())
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
    return jsonify(todotask=todo.to_dict())


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = db.session.query(ToDoTask).where(ToDoTask.id == todo_id).first()
    print('This is delete')
    return jsonify(todotask=todo.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
