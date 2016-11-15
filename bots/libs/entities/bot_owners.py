import time
from decimal import Decimal

from boto3.dynamodb.conditions import Key

from telegram.objects.user import TelegramUser
from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class OwnedBots(object):
    def __init__(self, user_id):
        self.user_id = user_id

    def add_bot(self, bot, token, timestamp=None):
        # TODO: make it async
        table = DynamoDB.get_table(DynamoDBTables.OWNED_BOTS)
        table.put_item(
           Item={
                'chat_id': self.user_id,
                'bot_id': bot.id,
                'info': {
                    'bot_name': bot.username,
                    'timestamp': timestamp if timestamp is not None else Decimal(time.time()),
                    'token': token,
                    'bot_user_str': bot.to_json_str(),
                }
            }
        )
        table = DynamoDB.get_table(DynamoDBTables.BOT_OWNER)
        table.put_item(
           Item={
                'bot_id': bot.id,
                'info': {'chat_id': self.user_id}
            }
        )

    def remove_bot(self, bot_id):
        table = DynamoDB.get_table(DynamoDBTables.OWNED_BOTS)
        table.delete_item(Key={'bot_id': bot_id, 'chat_id': self.user_id})
        table = DynamoDB.get_table(DynamoDBTables.BOT_OWNER)
        table.delete_item(Key={'bot_id': bot_id})

    def get_all_owned_bots(self):
        table = DynamoDB.get_table(DynamoDBTables.OWNED_BOTS)
        response = table.query(
            KeyConditionExpression=Key('chat_id').eq(self.user_id),
        )

        results = dict()
        for item in response[u'Items']:
            bot = TelegramUser.gen_from_json_str(item['info']['bot_user_str'])  # sub-optimal
            results[bot.id] = {
                'token': item['info']['token'],
                'bot_user_str': item['info']['bot_user_str'],
            }
        return results

    def get_bots_count(self):
        table = DynamoDB.get_table(DynamoDBTables.OWNED_BOTS)
        response = table.query(
            KeyConditionExpression=Key('chat_id').eq(self.user_id),
            Select='COUNT',
        )
        return int(response['Count'])

    def get_bot(self, bot_id):
        table = DynamoDB.get_table(DynamoDBTables.OWNED_BOTS)
        response = table.get_item(Key={'chat_id': self.user_id, 'bot_id': bot_id})
        item = response.get('Item')
        if item is None:
            return None

        return {
            'token': item['info']['token'],
            'bot_user_str': item['info']['bot_user_str'],
        }


    @classmethod
    def get_owner_for_bot(cls, bot_id):
        table = DynamoDB.get_table(DynamoDBTables.BOT_OWNER)
        response = table.get_item(Key={'bot_id': bot_id})
        item = response.get('Item')
        if item is None:
            return None

        return int(item['info']['chat_id'])


if __name__ == '__main__':
    user = TelegramUser(1, 'first', 'last', 'username')
    owner = OwnedBots(user.id)
    owner.add_bot(TelegramUser(2, 'first', 'last', 'bot2'), '23424')
    owner.add_bot(TelegramUser(3, 'first', 'last', 'bot3'), '34656')
    print owner.get_all_owned_bots()
    print owner.get_bots_count()
    owner.remove_bot(2)
    print owner.get_all_owned_bots()
    print OwnedBots.get_owner_for_bot(2)
    print OwnedBots.get_owner_for_bot(3)
