
from app.errors import bp as errors_bp
from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)


app.register_blueprint(errors_bp)

from app import routes