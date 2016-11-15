import boto3
import simplejson as json
import decimal


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class DynamoDBTables(object):
    BOTS_INFO = 'BotsInfo'
    BOTS_ADMINS = 'BotsAdmins'
    BOTS_SUBSCRIBERS = 'BotsSubscribers'
    OWNED_BOTS = 'OwnedBots'
    BOT_OWNER = 'BotOwner'
    BOT_CHANNELS = 'BotChannels'
    BOT_CUSTOM_COMMANDS = 'BotCustomCommands'
    SYSTEM_SETTINGS = 'SystemSettings'
    USER_STATE = 'UserState'
    BOT_USER_STATE = 'BotUserState'
    BOT_STATE = 'BotState'
    SCHEDULED_ASYNC_JOBS = 'ScheduledAsyncJobs'


class DynamoDB(object):
    _RESOURCE = None

    @classmethod
    def get_resource(cls):
        if cls._RESOURCE is None:
            cls._RESOURCE = boto3.resource(
                'dynamodb',
                region_name='eu-central-1',
                endpoint_url="https://dynamodb.eu-central-1.amazonaws.com")
        return cls._RESOURCE

    @classmethod
    def get_table(cls, table_name):
        resource = cls.get_resource()
        return resource.Table(table_name)


# called manually
def create_table_bots_info():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOTS_INFO,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Table status:", table.table_status)


def create_table_bots_subscribers():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOTS_SUBSCRIBERS,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'chat_id',
                'KeyType': 'RANGE'
            }

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Table status:", table.table_status)


def create_table_bots_admins():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOTS_ADMINS,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'chat_id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Table status:", table.table_status)


def create_table_owned_bots():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.OWNED_BOTS,
        KeySchema=[
            {
                'AttributeName': 'chat_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'bot_id',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Table status:", table.table_status)


def create_table_bot_owner():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOT_OWNER,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    print("Table status:", table.table_status)


def create_table_bot_channels():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOT_CHANNELS,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'channel',
                'KeyType': 'RANGE'
            }

        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'channel',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 3,
            'WriteCapacityUnits': 3
        }
    )

    print("Table status:", table.table_status)


def create_table_bot_custom_commands():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOT_CUSTOM_COMMANDS,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'command_id',
                'KeyType': 'RANGE'
            }
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'parent_id-index',
                'KeySchema': [
                    {
                        'AttributeName': 'bot_id',
                        'KeyType': 'HASH'  # Partition key
                    },
                    {
                        'AttributeName': 'parent_id',
                        'KeyType': 'RANGE',
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL',
                },
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'command_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'parent_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 25,
            'WriteCapacityUnits': 25
        }
    )

    print("Table status:", table.table_status)


def create_table_system_settings():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.SYSTEM_SETTINGS,
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    print("Table status:", table.table_status)


def create_table_user_state():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.USER_STATE,
        KeySchema=[
            {
                'AttributeName': 'chat_id',
                'KeyType': 'HASH'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'chat_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Table status:", table.table_status)


def create_table_bot_user_state():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOT_USER_STATE,
        KeySchema=[
            {
                'AttributeName': 'bot_id_chat_id',
                'KeyType': 'HASH'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id_chat_id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    print("Table status:", table.table_status)

def create_table_bot_state():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.BOT_STATE,
        KeySchema=[
            {
                'AttributeName': 'bot_id',
                'KeyType': 'HASH'  #Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'bot_id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 25,
            'WriteCapacityUnits': 25
        }
    )

    print("Table status:", table.table_status)


def create_table_scheduled_async_jobs():
    resource = DynamoDB.get_resource()

    table = resource.create_table(
        TableName=DynamoDBTables.SCHEDULED_ASYNC_JOBS,
        KeySchema=[
            {
                'AttributeName': 'async_id',
                'KeyType': 'HASH'  #Partition key
            },
            {
                'AttributeName': 'timestamp',
                'KeyType': 'RANGE'  #Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'async_id',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 25,
            'WriteCapacityUnits': 25
        }
    )

    print("Table status:", table.table_status)