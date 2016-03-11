from psycopg2.extras import Json
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)

from validations import logged_in_val, edit_date_val, order_val, get_week_val
from errors import BadRequestJSON

@app.route('/place_order', methods=['POST'])
@logged_in_val
@edit_date_val
@order_val
def place_order(user, date, order):
    # TODO: proper upsert
    data = {'userid': user['studentid'], 'day': date, 'price': 5,
            'restaurant': order['restaurant'], 'order_data': Json(order)}
    e_query = 'SELECT orderid FROM orders'\
        ' WHERE userid = %(userid)s AND day = %(day)s;'
    existing = db.engine.execute(e_query, data).first()
    if existing:
        data['orderid'] = existing['orderid']
        query = 'UPDATE orders SET '\
            'price = %(price)s, restaurant = %(restaurant)s, order_data = %(order_data)s'\
            ' WHERE orderid = %(orderid)s;'
    else:
        query = 'INSERT INTO orders VALUES (DEFAULT, '\
            '%(userid)s, %(day)s, %(price)s, %(restaurant)s, %(order_data)s);'
    db.engine.execute(query, data)
    resp = 'placed order at {}'.format(order['restaurant'])
    return jsonify(success=True, message=resp)

@app.route('/cancel_order', methods=['POST'])
@logged_in_val
@edit_date_val
def cancel_order(user, date):
    # TODO: proper upsert
    data = {'userid': user['studentid'], 'day': date}
    query = 'DELETE FROM orders WHERE userid = %(userid)s AND day = %(day)s;'
    res = db.engine.execute(query, data)
    if res.rowcount:
        return jsonify(success=True, message='deleted order')
    else:
        raise BadRequestJSON('no such order')

@app.route('/get_orders', methods=['POST'])
@logged_in_val
@get_week_val
def get_orders(user, week):
    data = {'userid': user['studentid'], 'week': week}
    query = 'SELECT o.order_data AS order, d.holiday'\
            ' FROM unnest(%(week)s) AS r (day)'\
                ' LEFT JOIN'\
                    ' (SELECT * FROM orders WHERE userid = %(userid)s)'\
                    ' AS o USING (day)'\
                ' LEFT JOIN days AS d USING (day)'\
                ' ORDER BY day;'
    res = db.engine.execute(query, data).fetchall()
    res = list(map(dict, res))
    return jsonify(success=True, days=res)

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
    """.format(app.config['CLIENT_ID'])

