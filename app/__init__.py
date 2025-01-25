from flask import Flask
from dotenv import load_dotenv
import logging

load_dotenv()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)

    #register blutprints
    from .main import main as main_blutprint
    app.register_blueprint(main_blutprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    
    return app