import os
import random
import string

from flask import Flask

from . import auth
from . import db
from . import posts

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)),
    DATABASE=os.path.join(app.instance_path, 'app.sqlite')
)

db.init_app(app)
app.register_blueprint(auth.bp)

app.register_blueprint(posts.bp)
app.add_url_rule('/', endpoint='index')
