from flask import Flask
from application import blueprint as api

app = Flask("__name__")

app.register_blueprint(api, url_prefix='/AuthorNews/v1')


app.run('0.0.0.0')