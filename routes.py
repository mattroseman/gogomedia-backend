from views.index import index
from views.user import user


def add_routes(app):
    app.add_url_rule('/', 'index', index)

    app.add_url_rule('/user', 'user', user, methods=['POST'])
