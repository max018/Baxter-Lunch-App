from flask import Flask

app = Flask(__name__)

from validations import order_val
from config import config

app.config.update(config)

