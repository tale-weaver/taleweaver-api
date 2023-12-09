import json
from bson import ObjectId
from datetime import datetime
from flask.json.provider import JSONProvider
from flask.wrappers import Response


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


class MongoJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=MongoJSONEncoder)

    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)
