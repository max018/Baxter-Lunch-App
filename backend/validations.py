from flask import abort, request
from errors import BadRequestJSON
from restaurants import restaurants

class Validator:
    def __init__(self, val):
        self.val = val

    def run(self):
        try:
            data = request.get_json()
            self.val(data)
            return data
        except BadRequest as e:
            raise BadRequestJSON('malformed JSON')
        except KeyError as e:
            raise BadRequest('missing key: {!r}'.format(e.args[0]))
        except AssertionError as e:
            raise BadRequest(*e.args)

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

