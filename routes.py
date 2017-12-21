from views.index import index


def add_routes(app):
    app.add_url_rule('/', 'index', index)
