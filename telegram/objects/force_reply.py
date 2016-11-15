# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramForceReply(TelegramObject):
    def __init__(self, selective=None):
        self.selective = bool(selective)

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramForceReply(selective=json_object.get('selective'))

    def to_json(self):
        result = {'force_reply': True}
        if self.selective is not None:
            result['selective'] = self.selective
        return result


if __name__ == '__main__':
    obj = TelegramForceReply.gen_from_json_str('{"force_reply": true, "selective": false}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.selective