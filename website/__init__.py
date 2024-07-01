from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import psycopg2
import os

DB_URI = os.environ.get('DATABASE_URI')
DB_SECRET_KEY = os.environ.get('DB_SECRET_KEY')

# Instanciar o SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configurações do Flask
    app.config['SECRET_KEY'] = DB_SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o SQLAlchemy com o app
    db.init_app(app)

    # Importar as views e autenticação
    from .views import views
    from .auth import auth

    # Registrar as blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    # Importar os modelos
    from .models import User, Category, Expense, Permission

    # Criar as tabelas no banco de dados
    with app.app_context():
        db.create_all()

    # Inicializar o LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Função para carregar o usuário
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
