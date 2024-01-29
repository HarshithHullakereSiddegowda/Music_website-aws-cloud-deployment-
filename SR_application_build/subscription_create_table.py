import boto3


def subscription_create_table(dynamodb = None):
    """
    Creates an Amazon DynamoDB table that can be used to store movie data.
    The table uses the release year of the movie as the partition key and the
    title as the sort key.
    :param table_name: The name of the table to create.
    :return: The newly created table.
    """
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        
    print(list(dynamodb.tables.all()))
    
    table = dynamodb.create_table(
        TableName='subscription',
        KeySchema=[
            {
            'AttributeName': 'email',
            'KeyType': 'HASH' # Partition key
            },
            {
            'AttributeName':'password' ,
            'KeyType': 'RANGE' # Sort key
            }

            ],
            AttributeDefinitions=[
            {
            'AttributeName': 'email',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'password',
            'AttributeType': 'S'
            },
            ],
            ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
            }
    )
    return table

# table = dynamodb.create_table(
#     TableName='subscription',
#     KeySchema=[        {            'AttributeName': 'email',            'KeyType': 'HASH' # Partition key        },    ],
#     AttributeDefinitions=[        {            'AttributeName': 'email',            'AttributeType': 'S'        },        {            'AttributeName': 'songs',            'AttributeType': 'SS' # Use 'SS' for Set of Strings        },    ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 10,
#         'WriteCapacityUnits': 10
#     },
#     GlobalSecondaryIndexes=[{        'IndexName': 'songs-index',        'KeySchema': [            {                'AttributeName': 'songs',                'KeyType': 'HASH'            }        ],
#         'Projection': {
#             'ProjectionType': 'ALL'
#         },
#         'ProvisionedThroughput': {
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     }]
# )



if __name__ == '__main__':
    music_table = subscription_create_table()
    print("Table status:", music_table.table_status)