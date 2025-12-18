from flask import Flask
from flask_cors import CORS

from app.db import db
from app.routes import api


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    # default configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # allow test overrides
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(api)

    @app.route("/")
    def home():
        return "Backend is running successfully"

    return app

# create a module-level app for convenience (e.g. dev usage and imports in tests)
app = create_app()

if __name__ == "__main__":
    # create tables only when running the module directly
    with app.app_context():
        db.create_all()
    app.run(debug=True)
