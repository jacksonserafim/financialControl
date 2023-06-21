from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .blueprint import register_blueprints

db = SQLAlchemy()
DB_NAME = 'financialSystem.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MUDAR DEPOIS'  # TODO: mudar quando for fazer o deploy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    register_blueprints(app)

    from .models import User, Category, Expense, Installment, Permission

    with app.app_context():
        db.create_all()

    return app
