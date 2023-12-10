from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from .resources import user, category, record

from project.db import db
from config import Config
from flask_migrate import Migrate

migrate = Migrate()
api = Api()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)
    api.init_app(app)

    from .resources.user import blp as user_blp
    api.register_blueprint(user_blp)

    from .resources.category import blp as category_blp
    api.register_blueprint(category_blp)

    from .resources.record import blp as record_blp
    api.register_blueprint(record_blp)

    from .resources.account import blp as account_blp
    api.register_blueprint(account_blp)

    return app


app = create_app()


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({'message': 'The token has expired.',
                 "error": "token_expired"}), 401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify({"message": "Signature verification failed.",
                 "error": "invalid_token"}), 401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify({"description": "Request does not contain an access token.",
                 "error": "authorization_required"}), 401,
    )


import project.views
