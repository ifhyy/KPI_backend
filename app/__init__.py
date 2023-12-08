from flask import Flask
from flask_smorest import Api
from .resources import user, category, record

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
api = Api()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

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

    return app

