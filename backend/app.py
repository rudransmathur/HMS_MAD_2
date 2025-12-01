from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_cors import CORS
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

from resources import *
from application import *
from app_celery import celery_init_app

def create_app():
    app = Flask(__name__)

    # Load .env file contents
    load_dotenv()

    # configure local development
    app.config.from_object(LocalDevConfig)

    # Database
    db.init_app(app)

    # allow requests from dev origin for all /api/* endpoints
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Authentication-Token"])

    datastore = SQLAlchemyUserDatastore(db, User, Role)

    # register_blueprint = False
    app.datastore = datastore

    print("CACHE TYPE:", type(cache))

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    # api.init_app(app)

    security.init_app(app, datastore=datastore)

    cache.init_app(app)

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

from datetime import datetime

@app.route('/cache')
@cache.cached()   # optional timeout
def cache_route(timeout=1):
    return {"date": str(datetime.utcnow())}


if __name__ == "__main__":
    app.run()
