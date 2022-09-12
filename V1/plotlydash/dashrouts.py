import dash
from flask.helpers import get_root_path

from V1.plotlydash.layout import Layout
from V1.plotlydash.callbacks import register_callbacks

def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/')

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)        


def init_dashRoutes(app):
    register_dashapp(app, 'Dashapp', 'AuthorNews/v1/dashboard', Layout, register_callbacks)

