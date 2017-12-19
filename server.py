from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/media', methods=['GET', 'POST'])
def add_media():
    if request.method == 'GET':
        # TODO grab all the media from the database and return it
        pass
    else:
        media_name = request.form['name']
        # TODO store this media in the database as unconsumed
