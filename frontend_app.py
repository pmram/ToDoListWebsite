import json
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
import requests

app = Flask(__name__)

bootstrap = Bootstrap5(app)
API_KEY = "TopSecretAPIKEY"
API_URL = "http://127.0.0.1:5000/API"


@app.route('/')
def home():
    response = requests.get(f"{API_URL}/todos")
    todos = json.loads(response.text).get('todos')
    return render_template('index.html', todos=todos)


if __name__ == "__main__":
    app.run()