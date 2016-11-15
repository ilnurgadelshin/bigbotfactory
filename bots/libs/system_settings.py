# -*- coding: utf-8 -*-

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class SystemSettings(object):
    @classmethod
    def set(cls, key, value):
        table = DynamoDB.get_table(DynamoDBTables.SYSTEM_SETTINGS)
        table.put_item(
           Item={
                'name': key,
                'info': {'value': value}, # isn't it silly?
            }
        )

    @classmethod
    def get(cls, key):
        table = DynamoDB.get_table(DynamoDBTables.SYSTEM_SETTINGS)
        response = table.get_item(Key={'name': key})
        item = response.get('Item')
        if item is None:
            return None
        return item['info'].get('value')

    @classmethod
    def remove(cls, key):
        table = DynamoDB.get_table(DynamoDBTables.SYSTEM_SETTINGS)
        table.delete_item(Key={'name': key})


if __name__ == '__main__':
    key = 'NEVER_USE_THIS_VALUE'
    SystemSettings.set(key, 'test_value')
    print SystemSettings.get(key)
    SystemSettings.remove(key)
    print SystemSettings.get(key)