from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)

from validations import logged_in_val, order_val

@app.route('/place_order', methods=['POST'])
@logged_in_val
@order_val
def place_order(user, order):
    resp = 'placed order at {}'.format(order['restaurant'])
    return jsonify(success=True, message=resp, for_=user)

@app.route('/get_orders', methods=['POST'])
@logged_in_val
def get_orders(user):
    return jsonify(success=True, orders=['placeholder'])

@app.route('/login')
def login():
    return """
<script src="https://apis.google.com/js/platform.js" async defer></script>
<meta name="google-signin-client_id" content="{}">
<script>
function onSignIn(googleUser) {{
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail());
  console.log('Token: ' + googleUser.getAuthResponse().id_token);
}}
</script>
<div class="g-signin2" data-onsuccess="onSignIn"></div>
    """.format(config['CLIENT_ID'])

