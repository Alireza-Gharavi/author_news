from flask_restx import Api
from flask import Blueprint, url_for


blueprint = Blueprint('authornews',__name__)


class MyApi(Api):
    @property
    def specs_url(self):
        """Monkey patch for HTTPS"""
        scheme = 'http' if '5000' in self.base_url else 'https'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)




from V1.authornews import api as authnews 
from V1.news_count import api as news_count


api = MyApi(blueprint,
            title='AuthorNews',
            version='1.0',
            description='Some Statiscal Analysis on Crypto News',
            )

api.add_namespace(authnews)
api.add_namespace(news_count)