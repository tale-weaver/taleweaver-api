import json
from bson import ObjectId
from datetime import datetime
from flask.json.provider import JSONProvider


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, dict):
            return {key: self.default(value) for key, value in o.items()}
        elif isinstance(o, list):
            return [self.default(element) for element in o]
        else:
            print(type(o))
            return super().default(o)


class MongoJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=MongoJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
