# -*- coding: utf-8 -*-
from functools import wraps


def consumes(content_type):
    def _consumes(function):
        @wraps(function)
        def __consumes(*argv, **keywords):
            if request.headers['Content-Type'] != content_type:
                abort(400)
            return function(*argv, **keywords)
        return __consumes
    return _consumes
