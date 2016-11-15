# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramUser(TelegramObject):
    def __init__(self, id, first_name, last_name=None, username=None):
        assert id is not None
        assert first_name is not None

        self.id = int(id)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramUser(
            id=json_object['id'],
            first_name=json_object['first_name'],
            last_name=json_object.get('last_name'),
            username=json_object.get('username'),
        )

    def to_json(self):
        result = {
            'id': self.id,
            'first_name': self.first_name,
        }
        if self.last_name is not None:
            result['last_name'] = self.last_name
        if self.username is not None:
            result['username'] = self.username
        return result


if __name__ == '__main__':
    user = TelegramUser.\
        gen_from_json_str('{"username": "lolipop", "first_name": "John", "last_name": "Smith", "id": 123456789}')
    print user.to_json()
    print user.to_json_str()
    print user.first_name
    print TelegramUser.gen_from_json({u'username': u'lolipop', u'first_name': u'John', u'last_name': u'Smith', u'id': 987654321})