# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramReplyKeyBoardHide(TelegramObject):
    def __init__(self, selective=None):
        self.selective = bool(selective) if selective is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramReplyKeyBoardHide(selective=json_object.get('selective'))

    def to_json(self):
        result = {'hide_keyboard': True}
        if self.selective is not None:
            result['selective'] = self.selective
        return result


if __name__ == '__main__':
    obj = TelegramReplyKeyBoardHide.gen_from_json_str('{"hide_keyboard": true, "selective": false}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.selective