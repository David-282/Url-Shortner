from flask import Flask
from flask_cors import CORS

from app.config import Config
from database import db, init_db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    init_db(app)

    from blueprint.url_bp import url_blueprint
    app.register_blueprint(url_blueprint)

    return app