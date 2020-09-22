from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)

from app.errors import bp as errors_bp

app.register_blueprint(errors_bp)

from app import routes