import boto3


def music_create_table(dynamodb = None):
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
        TableName='Music',
        KeySchema=[
            {
            'AttributeName': 'title',
            'KeyType': 'HASH' # Partition key
            },
            {
            'AttributeName':'artist' ,
            'KeyType': 'RANGE' # Sort key
            }

            ],
            AttributeDefinitions=[
            {
            'AttributeName': 'title',
            'AttributeType': 'S'
            },
            {
            'AttributeName': 'artist',
            'AttributeType': 'S'
            },
            ],
            ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
            }
    )
    return table




if __name__ == '__main__':
    music_table = music_create_table()
    print("Table status:", music_table.table_status)
    
    
                    
            


        