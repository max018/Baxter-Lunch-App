from flask import Flask, jsonify

app = Flask(__name__)

from validations import logged_in_val, order_val
from config import config

app.config.update(config)

@app.route('/order', methods=['POST'])
@logged_in_val
@order_val
def order(user, order):
    resp = 'placed order at {}'.format(order['restaurant'])
    return jsonify(success=True, message=resp)

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

