from telegram.objects.user import TelegramUser

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables
from telegram.api.core.api import TelegramAPIHandler
import time


def set_new_webhook(item):
    token = item['info']['token']
    bot_name = TelegramUser.gen_from_json_str(item['info']['bot_user_str']).username
    print 'reseting for: ' + token
    handler = TelegramAPIHandler(token)
    handler.set_webhook('https://balancer.example.com/bots/prod/BROADCAST_BOT/' + token + "/" + bot_name)
    time.sleep(0.1)


def main():
    table = DynamoDB.get_table(DynamoDBTables.OWNED_BOTS)
    response = table.scan()

    for item in response['Items']:
        set_new_webhook(item)

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ExclusiveStartKey=response['LastEvaluatedKey']
        )

        for item in response['Items']:
            set_new_webhook(item)



if __name__ == '__main__':
    main()
