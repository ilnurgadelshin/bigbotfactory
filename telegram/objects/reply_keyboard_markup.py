# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramReplyKeyBoardMarkup(TelegramObject):
    def __init__(self, keyboard, resize_keyboard=None, one_time_keyboard=None, selective=None):
        assert keyboard is not None
        self.keyboard = keyboard
        self.resize_keyboard = bool(resize_keyboard) if resize_keyboard is not None else None
        self.one_time_keyboard = bool(one_time_keyboard) if one_time_keyboard is not None else None
        self.selective = bool(selective) if selective is not None else None

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramReplyKeyBoardMarkup(
            keyboard=json_object['keyboard'],
            resize_keyboard=json_object.get('resize_keyboard'),
            one_time_keyboard=json_object.get('one_time_keyboard'),
            selective=json_object.get('selective'),
        )

    def to_json(self):
        result = {'keyboard': self.keyboard}
        if self.resize_keyboard is not None:
            result['resize_keyboard'] = self.resize_keyboard
        if self.one_time_keyboard is not None:
            result['one_time_keyboard'] = self.one_time_keyboard
        if self.selective is not None:
            result['selective'] = self.selective
        return result


if __name__ == '__main__':
    obj = TelegramReplyKeyBoardMarkup.gen_from_json_str('{"keyboard": [["\u666e\u4eac \u043f\u0443\u0442\u0438\u043d\u2764\ufe0f! \u067e\u0648\u062a\u06cc\u0646", "b"], ["c", "d", "e"]], "resize_keyboard": true, "one_time_keyboard": false, "selective": false}')
    print obj.keyboard[0][0]
    print type(obj.keyboard[0][0])
    print obj.to_json()
    print obj.to_json_str()
    obj = TelegramReplyKeyBoardMarkup.gen_from_json_str(obj.to_json_str())
    print obj.keyboard[0][0]
    print obj.resize_keyboard
    print obj.one_time_keyboard
    print obj.selective

    obj.keyboard[0][0] = u'❤️'
    obj = TelegramReplyKeyBoardMarkup.gen_from_json_str(obj.to_json_str())
    print obj.keyboard[0][0]
    print type(obj.keyboard[0][0])
    print obj.resize_keyboard
    print obj.one_time_keyboard
    print obj.selective

