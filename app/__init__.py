from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from redis import Redis
import logging
import os

load_dotenv()

limiter = Limiter(get_remote_address, storage_uri="redis://localhost:6379")

r = Redis(host=os.environ['HOST'], port=os.environ['PORT'],
                   db=os.environ['DB'], password=os.environ['PASSWORD'],
                   decode_responses=True)

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    #register blutprints
    limiter.init_app(app)
    from .main import main as main_blutprint
    app.register_blueprint(main_blutprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    
    return app