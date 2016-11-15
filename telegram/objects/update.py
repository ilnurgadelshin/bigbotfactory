# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject
from telegram.objects.message import TelegramMessage


class TelegramUpdate(TelegramObject):
    def __init__(self, update_id, message=None):
        assert update_id is not None

        self.update_id = int(update_id)
        self.message = message
        if message is not None:
            assert isinstance(message, TelegramMessage)

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramUpdate(
            update_id=json_object['update_id'],
            message=TelegramMessage.gen_from_json(json_object['message']) \
                if json_object.get('message') is not None else None
        )

    def to_json(self):
        result = {'update_id': self.update_id}
        if self.message is not None:
            result['message'] = self.message.to_json()
        return result


if __name__ == '__main__':
    obj = TelegramUpdate.gen_from_json_str('{"update_id":123456, "message":{"message_id":5,"from":{"id":44444,"first_name":"John","last_name":"Smith","username":"johnsmth"},"chat":{"id":44444,"first_name":"John","last_name":"Smith","username":"johnsmith"},"date":1437637248,"text":"\ud83d\ude22"}}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.update_id
    if obj.message is not None:
        print obj.message.text
        print obj.message.to_json_str()