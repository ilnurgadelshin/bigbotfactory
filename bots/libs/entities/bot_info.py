# -*- coding: utf-8 -*-

from telegram.objects.user import TelegramUser
from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class BotInfo(object):
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def set_about(self, about):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_INFO)
        table.put_item(
           Item={
                'bot_id': self.bot_id,
                'info': {
                    'about': about,
                }
            }
        )

    def get_about(self):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_INFO)
        response = table.get_item(Key={'bot_id': self.bot_id})
        item = response.get('Item')
        if item is None:
            return None

        return item['info']['about']


if __name__ == '__main__':
    user = TelegramUser(1, 'first', 'last', 'username')
    bot_info = BotInfo(1)
    bot_info.set_about(u'тест ⭐️⭐️⭐️⭐️⭐️ ')
    print bot_info.get_about()
    table = DynamoDB.get_table(DynamoDBTables.BOTS_INFO)
    response = table.delete_item(Key={'bot_id': 1})
    print bot_info.get_about()