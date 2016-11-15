from boto3.dynamodb.conditions import Key
from telegram.objects.user import TelegramUser
from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class BotAdmins(object):
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def add_admin(self, user, async=True):
        # TODO: use async
        table = DynamoDB.get_table(DynamoDBTables.BOTS_ADMINS)
        table.put_item(
           Item={
                'bot_id': self.bot_id,
                'chat_id': user.id,
                'info': {
                    'user_str': user.to_json_str(),
                }
            }
        )

    def remove_admin(self, chat_id):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_ADMINS)
        table.delete_item(Key={'bot_id': self.bot_id, 'chat_id': chat_id})

    def is_admin(self, chat_id):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_ADMINS)
        response = table.get_item(Key={'bot_id': self.bot_id, 'chat_id': chat_id})
        return response.get('Item') is not None

    def get_all_admins(self):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_ADMINS)
        response = table.query(
            KeyConditionExpression=Key('bot_id').eq(self.bot_id),
        )

        results = dict()
        for item in response[u'Items']:
            user = TelegramUser.gen_from_json_str(item['info']['user_str'])
            results[user.id] = user
        return results

    def get_admins_count(self):
        table = DynamoDB.get_table(DynamoDBTables.BOTS_ADMINS)
        response = table.query(
            KeyConditionExpression=Key('bot_id').eq(self.bot_id),
            Select='COUNT',
        )
        return int(response['Count'])


if __name__ == '__main__':
    user = TelegramUser(2, 'first', 'last', 'username')
    admins = BotAdmins(1)
    admins.add_admin(user)
    print admins.get_all_admins()
    admins.remove_admin(user.id)
    print admins.get_all_admins()
