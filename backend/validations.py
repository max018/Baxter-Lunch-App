from flask import abort, request
from werkzeug.exceptions import BadRequest
from errors import BadRequestJSON
from restaurants import restaurants

class Validator:
    def __init__(self, val):
        self.val = val

    def run(self):
        try:
            data = request.get_json()
            if data is None:
                raise BadRequestJSON('not a JSON request')
            result = self.val(data)
            if result is None:
                return data
            else:
                return result
        except BadRequest as e:
            raise BadRequestJSON('malformed JSON')
        except KeyError as e:
            raise BadRequestJSON('missing key: {!r}'.format(e.args[0]))
        except TypeError as e:
            raise BadRequestJSON('invalid request structure')
        except AssertionError as e:
            raise BadRequestJSON(*e.args)

@Validator
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

