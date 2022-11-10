from flask import Flask, jsonify, request

app = Flask(__name__)
API_KEY = "TopSecretAPIKEY"


@app.route('/')
def home():
    return "APP 1"


if __name__ == "__main__":
    app.run()