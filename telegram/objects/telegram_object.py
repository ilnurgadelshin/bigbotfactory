# -*- coding: utf-8 -*-
import simplejson as json


class TelegramObject(object):
    @classmethod
    def gen_from_json_str(cls, json_string):
        return cls.gen_from_json(json.loads(json_string, encoding='utf8'))

    @classmethod
    def gen_from_json(cls, json_object):
        assert isinstance(json_object, dict)
        return cls._gen_from_json(json_object)

    def to_json_str(self):
        return json.dumps(self.to_json()).encode('utf8')

    @classmethod
    def _gen_from_json(cls, json_object):
        raise NotImplementedError()

    def to_json(self):
        raise NotImplementedError()
