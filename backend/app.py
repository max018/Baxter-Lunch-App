from sqlalchemy.exc import IntegrityError
from psycopg2.extras import Json
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
from config import config

app = Flask(__name__)
app.config.update(config)
db = SQLAlchemy(app)
CORS(app)

from validations import logged_in_val, edit_date_val, order_val, get_week_val
from errors import BadRequestJSON

@app.route('/place_order', methods=['POST'])
@logged_in_val
@edit_date_val
@order_val
def place_order(student, date, order):
    data = {'studentid': student['studentid'], 'day': date, 'price': 5,
            'restaurant': order['restaurant'], 'order_data': Json(order)}
    query = 'INSERT INTO orders VALUES (DEFAULT, '\
        '%(studentid)s, %(day)s, %(price)s, %(restaurant)s, %(order_data)s);'
    try:
        db.engine.execute(query, data)
        resp = 'placed order at {}'.format(order['restaurant'])
        return jsonify(success=True, message=resp)
    except IntegrityError:
        raise BadRequestJSON('conflicting order exists')

@app.route('/cancel_order', methods=['POST'])
@logged_in_val
@edit_date_val
def cancel_order(student, date):
    data = {'studentid': student['studentid'], 'day': date}
    query = 'DELETE FROM orders'\
        ' WHERE studentid = %(studentid)s AND day = %(day)s;'
    res = db.engine.execute(query, data)
    if res.rowcount:
        return jsonify(success=True, message='deleted order')
    else:
        raise BadRequestJSON('no such order')

@app.route('/get_orders', methods=['POST'])
@logged_in_val
@get_week_val
def get_orders(student, week):
    data = {'studentid': student['studentid'], 'week': week}
    query = 'SELECT o.order_data AS order, d.holiday'\
            ' FROM unnest(%(week)s) AS r (day)'\
                ' LEFT JOIN'\
                    ' (SELECT * FROM orders WHERE studentid = %(studentid)s)'\
                    ' AS o USING (day)'\
                ' LEFT JOIN days AS d USING (day)'\
                ' ORDER BY day;'
    res = db.engine.execute(query, data).fetchall()
    res = list(map(dict, res))
    return jsonify(success=True, days=res)

