from flask import Flask

app = Flask(__name__)

from validations import order_val

