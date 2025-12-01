from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_cors import CORS
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
import logging

from application import *
from app_celery import celery_init_app
from resources import *
from services.scheduled_jobs import init_scheduler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)

    # Load .env file contents
    load_dotenv()

    # configure local development
    app.config.from_object(LocalDevConfig)

    # Database
    db.init_app(app)

    from flask_cors import CORS

    # allow requests from dev origin for all /api/* endpoints
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Authentication-Token"])

    security = Security()
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    # register_blueprint = False
    app.datastore = datastore

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    # api.init_app(app)

    # Initialize scheduler for background jobs
    with app.app_context():
        init_scheduler(app)

    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/1",
            timezone = 'Asia/Kolkata'
        ),
    )
    celery_app = celery_init_app(app)

    from tasks.test import add_func

    @app.route("/celery-task")
    def task():
        add_func.delay(1,2)
        return {"message":"task started"}
    
    @celery_app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        sender.add_periodic_task(1.0, add_func.s(1,2), name='add every 10')

    return app, celery_app

app, celery_app = create_app()

if __name__ == "__main__":
    app.run()
