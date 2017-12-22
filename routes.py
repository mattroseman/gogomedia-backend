from views.index import index
from views.user import user
from views.media import media


def add_routes(app):
    app.add_url_rule('/', 'index', index)

    app.add_url_rule('/user', 'user', user, methods=['POST'])

    app.add_url_rule('/user/<username>/media', 'media', media, methods=['POST'])
