# -*- coding: utf-8 -*-
from telegram.objects.telegram_object import TelegramObject


class TelegramResponse(TelegramObject):
    ERROR_CODE_EXCEPTION = 10001
    ERROR_CODE_KICKED_FROM_CHAT = 403

    def __init__(self, ok, description=None, result=None, error_code=None):
        assert ok is not None
        if result is not None:
            assert (isinstance(result, dict) or isinstance(result, list) or isinstance(result, bool))
        self.ok = bool(ok)
        self.description = description
        self.result = result
        self.error_code = int(error_code) if error_code is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramResponse(
            ok=json_object['ok'],
            description=json_object.get('description'),
            result=json_object.get('result'),
            error_code=json_object.get('error_code'),
        )

    def to_json(self):
        raise NotImplementedError("You never need a Response object in json format")
