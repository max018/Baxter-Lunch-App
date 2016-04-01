from flask import abort, request
from werkzeug.exceptions import BadRequest
from errors import BadRequestJSON
from app import app, db
from week import Week
import datetime

from functools import wraps
from oauth2client import client, crypt
from restaurants import restaurants

def assert_type(v, t):
    assert isinstance(v, t), '{!r} is not a {}'.format(v, t.__name__)

class Validator:
    @classmethod
    def with_key(cls, key):
        def wrapper(val):
            return cls(val, key=key)
        return wrapper

    def __init__(self, val, key=None):
        self.val = val
        self.key = key

    def run(self, data):
        try:
            if self.key is not None:
                data = data[self.key]
            res = self.val(data)
            if res is None:
                return data
            else:
                return res
        except KeyError as e:
            raise BadRequestJSON('missing key: {!r}'.format(e.args[0]))
        except TypeError as e:
            raise BadRequestJSON('invalid request structure')
        except AssertionError as e:
            raise BadRequestJSON(*e.args)

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = request.get_json()
                if data is None:
                    raise BadRequestJSON('not a JSON request')
                res = self.run(data)
            except BadRequest as e:
                raise BadRequestJSON('malformed JSON')
            return f(*args + (res,), **kwargs)
        return wrapper

def adjusted_min_edit():
    min = app.config['MIN_WEEKS_EDIT']
    if datetime.date.today().weekday() >= 4:
        min += 1
    return min

def verify_token(data):
    if app.debug:
        return data
    try:
        assert_type(data, str)
        token = bytes(data, 'utf-8')
        idinfo = client.verify_id_token(token, app.config['CLIENT_ID'])
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

        email = idinfo['email']
        return email
    except crypt.AppIdentityError as e:
        raise BadRequestJSON(*e.args)

@Validator.with_key('token')
def logged_in_val(data):
    email = verify_token(data)
    query = 'SELECT * FROM students WHERE email = %s;'
    student = db.engine.execute(query, email).first()
    assert student is not None, 'unknown student'
    return student

@Validator.with_key('token')
def admin_val(data):
    email = verify_token(data)
    assert email == app.config['ADMIN'], 'not an admin'

@Validator
def edit_date_val(data):
    week_offset, day = data['week_offset'], data['day']
    assert_type(week_offset, int)
    assert_type(day, int)
    min, max = adjusted_min_edit(), app.config['MAX_WEEKS']
    assert min <= week_offset <= max, 'week of order out of range'

    week = Week.from_offset(week_offset)
    date = week.day(day)

    query = 'SELECT holiday FROM days WHERE day = %s;'
    holiday = db.engine.execute(query, date).first()
    assert holiday is None, 'no lunch on date given'

    return date

@Validator.with_key('order')
def order_val(data):
    assert data['restaurant'] in restaurants, 'no such restaurant'
    restaurant = restaurants[data['restaurant']]
    if restaurant['simple']:
        assert data['option'] in restaurant['options'], 'nonexistent option'
    else:
        amounts = restaurant['meals'][data['meal']]
        for (group, amount) in amounts.items():
            group_choices = data['choices'][group]
            assert len(group_choices) == amount,\
                    'wrong number choices for group {!r}'.format(group)
            group_options = restaurant['groups'][group]
            assert all(item in group_options for item in group_choices),\
                    'nonexistent item chosen in group {!r}'.format(group)

@Validator.with_key('week_offset')
def get_week_val(week_offset):
    assert_type(week_offset, int)
    min, max = app.config['MIN_WEEKS_GET'], app.config['MAX_WEEKS']
    assert min <= week_offset <= max, 'week out of range'

    week = Week.from_offset(week_offset)
    return week

@Validator.with_key('offset')
def offset_val(offset):
    assert_type(offset, int)
    assert offset >= 0, 'negative offset'

@Validator.with_key('restaurant')
def restaurant_val(restaurant):
    if restaurant is None:
        return False
    assert_type(restaurant, str)
    for r in restaurants.keys():
        if restaurant.lower() in r.lower():
            return r
    else:
        raise BadRequestJSON('no such restaurant')

