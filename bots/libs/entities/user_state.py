# -*- coding: utf-8 -*-

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class UserState(object):
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.table = DynamoDB.get_table(DynamoDBTables.USER_STATE)
        self._initialized = False
        self.item = None

    def _initialize(self):
        if not self._initialized:
            self.item = self.table.get_item(Key={'chat_id': self.chat_id}).get('Item')
            self._initialized = True

    def set_value(self, key, value):
        self._initialize()
        if self.item is None:
            self.table.put_item(
                Item={
                    'chat_id': self.chat_id,
                    'info': {key: value}
                })
            self.item = {'info': {}}
        else:
            self.table.update_item(
                Key={'chat_id': self.chat_id},
                UpdateExpression="set info." + key + " = :v",
                ExpressionAttributeValues={':v': value},
            )
        self.item['info'][key] = value

    def remove_key(self, key):
        self._initialize()
        if self.item is None:
            return
        self.table.update_item(
            Key={'chat_id': self.chat_id},
            UpdateExpression="remove info." + key,
        )
        if key in self.item['info']:
            self.item['info'].pop(key)

    def get_value(self, key, default_value=None):
        self._initialize()
        if self.item is None:
            return default_value
        return self.item['info'].get(key, default_value)

    def __contains__(self, key):
        self._initialize()
        if self.item is None:
            return False
        else:
            return key in self.item['info']


if __name__ == '__main__':
    state = UserState(1)
    print state.get_value('key1')
    state.set_value('key1', 's345')
    print state.get_value('key1')
    state.set_value('key1', 345)
    print state.get_value('key1')
    state.set_value('key1', 342)
    print state.get_value('key1')
    state.set_value('key1', None)
    print state.get_value('key1')
    print 'key1' in state

    print "\n"
    print state.get_value('key3', 'some default value')
    state.set_value('key3', 'ppp')
    print state.get_value('key3', 'another default value')
    state.set_value('key3', [1, 2, 3, 4, 5])
    print type(state.get_value('key3', 'yet another default value'))
    state.set_value('key3', [])
    print type(state.get_value('key3', 'yet another default value'))
    print 'key3' in state
    print 'unexisting key' in state
    state.remove_key('key3')


