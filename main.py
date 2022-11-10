from werkzeug.middleware.dispatcher import DispatcherMiddleware
from frontend_app import app as frontend
from backend_app import app as backend
from flask import Flask

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(frontend, {
    '/API': backend
})

if __name__ == "__main__":
    app.run()

