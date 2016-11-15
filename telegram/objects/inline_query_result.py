# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramInlineQueryResult(TelegramObject):
    @classmethod
    def _gen_from_json(cls, json_object):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError

