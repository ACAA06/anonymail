import os

from flask import Flask

from . import auth
from . import db
from . import posts

app = Flask(__name__, static_folder=None)
app.config.from_mapping(SECRET_KEY='rajkumaar', DATABASE=os.path.join(app.instance_path, 'anonymail.sqlite'))

db.init_app(app)
app.register_blueprint(auth.bp)

app.register_blueprint(posts.bp)
app.add_url_rule('/', endpoint='index')
