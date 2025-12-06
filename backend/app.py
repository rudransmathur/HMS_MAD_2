from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_cors import CORS
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

from application import *
from app_celery import celery_init_app
from resources import *
from application.extension import cache


def create_app():
    app = Flask(__name__)

    # Load .env file contents
    load_dotenv()

    # Configure local development
    app.config.from_object(LocalDevConfig)

    # Configure Database
    db.init_app(app)

    # Configure cache
    app.config.setdefault('CACHE_TYPE', 'RedisCache')
    app.config.setdefault('CACHE_DEFAULT_TIMEOUT', 300)
    cache.init_app(app)

    # CORS
    from flask_cors import CORS

    CORS(app, resources={r"/api/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Authentication-Token"])

    # Security
    security = Security()
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    app.datastore = datastore

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)


    # Backend celery configuraation
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/1",
            timezone = 'Asia/Kolkata'
        ),
    )
    celery_app = celery_init_app(app)

    return app, celery_app


app, celery_app = create_app()

from tasks.test import add_func
@app.route("/celery-task")
def task():
    add_func.delay(1,2)
    return {"message": "task started"}


@celery_app.on_after_configure.connect
def periodic_task(sender:Celery, **kwargs):
    sender.add_periodic_task(10.0, add_func(1,5), name='add every 10')

    sender.add_periodic_task(30.0, add_func(2,3), expires=10)

    sender.add_periodic_task(
        crontab(minute=22,hour=23,day_of_week=1,),
        add_func(10,10)
    )

if __name__ == "__main__":
    app.run()
