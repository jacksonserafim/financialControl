from .views import views
from .auth import auth


def register_blueprints(app):
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
