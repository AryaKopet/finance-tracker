from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from database import Base, engine
# from models import User
from routes import init_auth_routes
from routes.transaction_routes import transaction_bp   
# from .utils import allowed_file

import os

db = SQLAlchemy()
Base.metadata.create_all(bind=engine)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = "supersecretkey"

    # Register blueprint
    app.register_blueprint(transaction_bp) 

    db.init_app(app)
    init_auth_routes(app, db)

    @app.route("/")
    def home():
        return redirect(url_for("login"))

    return app

if __name__ == "__main__":
    app = create_app()
    if not os.path.exists("instance"):
        os.mkdir("instance")
    app.run(debug=True)
