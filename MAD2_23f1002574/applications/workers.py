from celery import Celery
from flask import current_app as app

celery=Celery("Application jobs")

class ContextTask(celery.Task):
    _flask_app = None  # Class-level variable to store the Flask app reference

    def __call__(self, *args, **kwargs):
        if not self._flask_app:
            raise RuntimeError("Flask application is not initialized in the Celery worker.")
        with self._flask_app.app_context():
            return self.run(*args, **kwargs)