# -*- coding: utf-8 -*-

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class BotState(object):
    def __init__(self, bot_id):
        self.bot_id = bot_id
        self.table = DynamoDB.get_table(DynamoDBTables.BOT_STATE)
        self._initialized = False
        self.item = None

    def _initialize(self):
        if not self._initialized:
            self.item = self.table.get_item(Key={'bot_id': self.bot_id}).get('Item')
            self._initialized = True

    def set_value(self, key, value):
        self._initialize()
        if self.item is None:
            self.table.put_item(
                Item={
                    'bot_id': self.bot_id,
                    'info': {key: value}
                })
            self.item = {'info': {}}
        else:
            self.table.update_item(
                Key={'bot_id': self.bot_id},
                UpdateExpression="set info." + key + " = :v",
                ExpressionAttributeValues={':v': value},
            )
        self.item['info'][key] = value

    def get_value(self, key, default_value=None):
        self._initialize()
        if self.item is None:
            return default_value
        return self.item['info'].get(key, default_value)

    def remove_key(self, key):
        self._initialize()
        if self.item is None:
            return
        self.table.update_item(
            Key={'bot_id': self.bot_id},
            UpdateExpression="remove info." + key,
        )
        if key in self.item['info']:
            self.item['info'].pop(key)

    def __contains__(self, key):
        self._initialize()
        if self.item is None:
            return False
        else:
            return key in self.item['info']


if __name__ == '__main__':
    state = BotState(1)
    print state.get_value('key1')
    state.set_value('key1', 's345')
    print state.get_value('key1')
    state.set_value('key1', 345)
    print state.get_value('key1')
    state.set_value('key1', 342)
    print state.get_value('key1')
    state.set_value('key1', None)
    print state.get_value('key1')

    print '\n'
    print 'key1' in state
    print 'key2' in state

    print state.get_value('key4', 'some default value')
    state.set_value('key4', 'ppp')
    print state.get_value('key4', 'another default value')
    state.set_value('key4', 'qqq')
    print state.get_value('key4', 'yet another default value')
    print 'key4' in state
    print 'unexisting key' in state
    state.remove_key('key4')

