from boto3.dynamodb.conditions import Key

from lib.dynamodb.dynamo_db import DynamoDB, DynamoDBTables


class BotChannels(object):
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def add_channel(self, channel):
        # TODO: make it async
        table = DynamoDB.get_table(DynamoDBTables.BOT_CHANNELS)
        table.put_item(
           Item={
                'bot_id': self.bot_id,
                'channel': channel,
            }
        )

    def remove_channel(self, channel):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CHANNELS)
        table.delete_item(Key={'bot_id': self.bot_id, 'channel': channel})

    def get_all_channels(self):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CHANNELS)
        response = table.query(
            KeyConditionExpression=Key('bot_id').eq(self.bot_id),
        )

        results = list()
        for item in response[u'Items']:
            results.append(item['channel'])
        return results

    def has_channel(self, channel_name):
        table = DynamoDB.get_table(DynamoDBTables.BOT_CHANNELS)
        response = table.get_item(Key={'bot_id': self.bot_id, 'channel': channel_name})
        return response.get('Item') is not None


if __name__ == '__main__':
    channels = BotChannels(1)
    channels.add_channel('channel1')
    channels.add_channel('channel2')
    channels.add_channel('channel1')
    print channels.get_all_channels()
    channels.remove_channel('channel1')
    print channels.get_all_channels()
