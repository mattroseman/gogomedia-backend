from login_manager import login_manager

from views.index import index
from views.user import register, login, logout
from views.media import media

from models.user import User


def add_routes(app):
    app.add_url_rule('/', 'index', index)

    app.add_url_rule('/register', 'register', register, methods=['POST'])

    app.add_url_rule('/login', 'login', login, methods=['POST'])
    app.add_url_rule('/logout', 'logout', logout, methods=['GET'])

    app.add_url_rule('/user/<username>/media', 'media', media, methods=['PUT', 'GET', 'DELETE'])


@login_manager.user_loader
def user_loader(user_id):
    """
    user_loader takes a unique user id, and returns the associated user instance
    """
    return User.query.get(user_id)
