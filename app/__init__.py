import logging
from logging.config import dictConfig

from flask import Flask
from flask.logging import default_handler

from config import LOGGING, Configuration

dictConfig(LOGGING)
app = Flask(__name__)

app.logger = logging.getLogger('NLP')
app.logger.removeHandler(default_handler)
app.config.from_object(Configuration)

from app import views  