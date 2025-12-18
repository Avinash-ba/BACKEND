from flask import Flask
from flask_cors import CORS

from app.db import db
from app.routes import api

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(api)

@app.route("/")
def home():
    return "Backend is running successfully"

if __name__ == "__main__":
    app.run(debug=True)
