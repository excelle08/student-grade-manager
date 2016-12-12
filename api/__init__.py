# -*- coding: utf-8 -*-
import json


class APIError(Exception):
    status_code = 500

    def __init__(self, message, status_code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


def to_dict(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your conversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__dict__.keys():
        if c.startswith('_'):
            continue
        v = getattr(inst, c)
        if type(v) in convert.keys() and v is not None:
            try:
                d[c] = convert[c.type](v)
            except:
                d[c] = "Error:  Failed to covert using ", str(convert[type(v)])
        elif v is None:
            d[c] = str()
        else:
            d[c] = v
    return d


def to_json(inst, cls):
    """
    Jsonify the sql alchemy query result.
    """
    convert = dict()
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    d = dict()
    for c in cls.__dict__.keys():
        if c.startswith('_'):
            continue
        v = getattr(inst, c)
        if type(v) in convert.keys() and v is not None:
            try:
                d[c] = convert[c.type](v)
            except:
                d[c] = "Error:  Failed to covert using ", str(convert[type(v)])
        elif v is None:
            d[c] = str()
        else:
            d[c] = v
    return json.dumps(d)


class Base():

    def __init__(self):
        pass

    @property
    def json(self):
        return to_json(self, self.__class__)

    @property
    def dict(self):
        return to_dict(self, self.__class__)


def enum(**enums):
    return type('Enum', (), enums)


def get_arg(kwargs, key, default=None):
    if key in kwargs:
        return kwargs[key]
    else:
        if default is None:
            raise APIError('Missing parameter: %s' % key, status_code=400)
        return default
