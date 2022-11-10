from flask import Flask, jsonify, request
from werkzeug.serving import run_simple

app = Flask(__name__)
API_KEY = "TopSecretAPIKEY"


@app.route('/')
def home():
    return "APP 1"


if __name__ == "__main__":
    app.run()