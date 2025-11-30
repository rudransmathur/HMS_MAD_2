from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security.datastore import SQLAlchemyUserDatastore
from flask_cors import CORS
from dotenv import load_dotenv

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

    return app

app = create_app()

from datetime import datetime

@app.route('/cache')
@cache.cached()   # optional timeout
def cache_route(timeout=1):
    return {"date": str(datetime.utcnow())}


if __name__ == "__main__":
    app.run()
