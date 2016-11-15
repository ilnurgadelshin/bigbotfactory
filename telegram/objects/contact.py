# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramContact(TelegramObject):
    def __init__(self, phone_number, first_name, last_name=None, user_id=None):
        assert phone_number is not None
        assert first_name is not None

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = int(user_id) if user_id is not None else None  # bot's documentation lies here

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramContact(
            phone_number=json_object['phone_number'],
            first_name=json_object['first_name'],
            last_name=json_object.get('last_name'),
            user_id=json_object.get('user_id'),
        )

    def to_json(self):
        result = {
            'phone_number': self.phone_number,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_id': self.user_id,
        }
        return result


if __name__ == '__main__':
    obj = TelegramContact.gen_from_json_str('{"phone_number":"111222333","first_name":"John","last_name":"Smith","user_id": 111}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.phone_number
    print obj.first_name
    print obj.last_name
    print obj.user_id