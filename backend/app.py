from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_security.datastore import SQLAlchemyUserDatastore
from dotenv import load_dotenv

from application import *

from resources import *
from application import *

def create_app():
    app = Flask(__name__)

    # Load .env file contents
    load_dotenv()

    # configure local development
    app.config.from_object(LocalDevConfig)

    # Database
    db.init_app(app)

    # Security
    security = Security()
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore=datastore)

    # register_blueprint = False
    app.datastore = datastore

    app.register_blueprint(auth_bp)

    # api.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run()
