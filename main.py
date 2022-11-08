from datetime import datetime
import os
from flask import Flask, jsonify, request, render_template, redirect
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


@app.route('/todotasks', methods=['GET'])
def get_all_tasks():
    todotasks = db.session.query(ToDoTask).all()
    todotasks_json = [task.to_dict() for task in todotasks]
    return jsonify(todotasks=todotasks_json)


if __name__ == '__main__':
    app.run(debug=True)