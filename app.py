# app.py

import os
from flask import Flask,current_app
from applications.config import LocalDevelopmentConfig
from applications.database import init_db
from applications.controllers import setup_routes 
from applications import workers

app = None
celery=None

def create_app():
    app = Flask(__name__, template_folder="templates",static_folder='static')
    if os.getenv('ENV', "development") == "production":
        raise Exception("it's not for production")
    else:
        print("starting local development")
        app.config.from_object(LocalDevelopmentConfig)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/suneh/MAD2_23f1002574/db_directory/household.db'  # Replace with your actual database URI
    
    init_db(app)
    setup_routes(app)
    app.app_context().push() 
    celery=workers.celery
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask  # Use the custom ContextTask
    workers.ContextTask._flask_app = app 
    app.app_context().push() 

    return app,celery

app,celery= create_app()
app.app_context().push() 
app.jinja_env.variable_start_string = '{('
app.jinja_env.variable_end_string = ')}'
app.jinja_env.block_start_string = '{%'
app.jinja_env.block_end_string = '%}'



if __name__ == '__main__':
    app.run(threaded=False)