from flask import json, render_template
from peewee import datetime as peewee_datetime

from utils import get_request_data


peewee_now = peewee_datetime.datetime.now


class _Controller(object):
    def __init__(self, request):
        self.request = request
        self.request_data = get_request_data(self.request)

    def call(self, *args, **kwargs):
        data = "Error("
        try:
            if self.request.method == "GET":
                data = self._get(*args, **kwargs)
            else:
                data = self._post(*args, **kwargs)
        except Exception as ex:
            print(str(ex))
            print("Error during %s call" % self.__class__.__name__)
        finally:
            return data

    def _get(self, *args, **kwargs):
        raise NotImplementedError("_get from %s" % self.__class__.__name__)

    def _post(self, *args, **kwargs):
        raise NotImplementedError("_post from %s" % self.__class__.__name__)
