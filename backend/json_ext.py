import datetime
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return str(o)
        return super().default(o)

