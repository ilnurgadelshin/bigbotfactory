# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject


class TelegramChat(TelegramObject):
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"

    def __init__(self, id, type=None, title=None, username=None, first_name=None, last_name=None):
        assert id is not None
        assert type == self.PRIVATE or type == self.GROUP or type == self.SUPERGROUP or \
               type == self.CHANNEL or type is None
        self.id = int(id)
        self.type = type  # it can be None for back compatibility
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name


    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramChat(
            id=json_object['id'],
            type=json_object.get('type'),
            title=json_object.get('title'),
            username=json_object.get('username'),
            first_name=json_object.get('first_name'),
            last_name=json_object.get('last_name'),
        )

    def to_json(self):
        result = {'id': self.id}
        if self.type is not None:
            result['type'] = self.type
        if self.title is not None:
            result['title'] = self.title
        if self.username is not None:
            result['username'] = self.username
        if self.first_name is not None:
            result['first_name'] = self.first_name
        if self.last_name is not None:
            result['last_name'] = self.last_name
        return result

if __name__ == '__main__':
    obj = TelegramChat.gen_from_json_str('{"title": "John", "id": 555334, "type": "private"}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.title
    print obj.type