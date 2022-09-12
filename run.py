from flask import Flask
from V1 import blueprint as api
from flask_cors import CORS

from V1.plotlydash.dashrouts import init_dashRoutes


app = Flask("__name__")



app.register_blueprint(api, url_prefix='/AuthorNews/v1')

init_dashRoutes(app)
#app = init_dashboard(app)

CORS(app, resources={r"/*": {"origins":"*"}})

if __name__ == "__main__" :
    app.run(host='0.0.0.0', port=5000)

