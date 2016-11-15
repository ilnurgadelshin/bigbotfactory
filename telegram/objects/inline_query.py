# -*- coding: utf-8 -*-

from telegram.objects.telegram_object import TelegramObject
from telegram.objects.user import TelegramUser


class TelegramInlineQuery(TelegramObject):
    def __init__(self, id_, from_, query, offset):
        assert id_ is not None
        assert query is not None
        assert offset is not None

        self.id_ = id_
        self.from_ = from_
        assert isinstance(from_, TelegramUser)
        self.query = query
        self.offset = offset

    @classmethod
    def _gen_from_json(cls, json_object):
        return TelegramInlineQuery(
            id_=json_object['id'],
            from_=TelegramUser.gen_from_json(json_object['from']),
            query=json_object['query'],
            offset=json_object['offset'],
        )

    def to_json(self):
        result = {'id': self.id_, 'from': self.from_.to_json(), 'query': self.query, 'offset': self.offset}
        return result


if __name__ == '__main__':
    obj = TelegramInlineQuery.gen_from_json_str('{"id": "123213", "from":{"id":123456789,"first_name":"JOHN","last_name":"SMITH","username":"johnsmith"}, "query": "THIS IS QUERY", "offset": ""}')
    print obj.to_json()
    print obj.to_json_str()
    print obj.id_
    print obj.from_.to_json()
    print obj.query
    print obj.offset
