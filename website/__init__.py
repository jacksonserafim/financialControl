from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = 'financeSystem.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'MUDAR DEPOIS' # TODO: mudar quando for fazer o deploy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
