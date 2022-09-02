from flask import Flask
from application import blueprint as api
from flask_cors import CORS

app = Flask("__name__")

app.register_blueprint(api, url_prefix='/AuthorNews/v1')

CORS(app, resources={r"/*": {"origins":"*"}})

if __name__ == "__main__" :
    app.run(host='0.0.0.0', port=5000)