import boto3
from boto3 import resource
import config
from boto3.dynamodb.conditions import Key
from functools import reduce
from botocore.exceptions import ClientError
import logging





AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
SESSION_ID=config.SESSION_ID
#controller to aws dynamo db table using boto3 resource
 
 
data = boto3.resource(
   'dynamodb', 

   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME,
   aws_session_token = SESSION_ID
)


def read_login(email, password):#read the login_table data, dynamo db created on aws using resource.Table and get the items using key{:}
    login = data.Table('login')
    #print(login)
    response = login.get_item(
       Key = {
           'email': email,'password': password
       }
      
    )
    #print(response)
    
    return response



def newuser_dynamodb(email, username, password ):
    table =  data.Table('login')
    table.put_item(Item={
        'email':email,
        'user_name':username,
        'password':password
        })
    
def scan_music(title,artist, year):

    
    table=data.Table('Music')
    query_params = {}
    
    if title:
        query_params['title'] = title

    if year:
        query_params['year'] = year

    if artist:
        query_params['artist'] = artist
    print(query_params)
    scan_kwargs = {
        'FilterExpression': reduce(lambda x, y: x & y, [Key(k).eq(v) for k, v in query_params.items()]),
        'ProjectionExpression': "#yr, title, artist",
        'ExpressionAttributeNames': {"#yr": "year"}
    }
    print(scan_kwargs)
    done = False
    start_key = None
    items=[]

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey']= start_key
        
        try:

            response = table.scan(**scan_kwargs)
            items +=response.get('Items',[])
            start_key=response.get('LastEvaluatedKey', None)
            done=start_key is None
        except Exception as e:
            print(f"Error scanning table: {e}")
            return None
        
    if not items:
        return None
        
    
    print(items)
    return items

def put_music(email, password,subscribed_music, dynamodb=None):
    table = data.Table('subscription')
    response = table.get_item(
        Key={
        'email': email,
        'password':password
        }
    )
    
    if 'Item' in response:
        # print(f"{email} is already subscribed.")
        # return
        subscribed_music_old = response['Item'].get('songs',[])
        if subscribed_music:
            subscribed_music_dict=subscribed_music[0]

            subscribed_music_old.append(subscribed_music_dict)

            response = table.update_item(
                Key={'email': email, 'password':password},
                UpdateExpression='SET songs = :val',
                ExpressionAttributeValues={':val': subscribed_music_old}
            )
        print(f"Successfully updated subscription for {email}")
    elif 'Item' not in response:
        response = table.put_item(
            Item={
                'email': email,
                'password':password,
                'songs': subscribed_music
            }
        )
        print(f"Successfully created subscription for {email}")


def get_subscribed_music(email, password):


    table=data.Table('subscription')
    response= table.get_item(
        Key={'email':email,'password':password}
    )
    #print(response['Item']['songs'])
    if 'Item' in response:
        return response['Item']['songs']
    else:
        return None
    

    
def  remove(email, password,subscribed_music, dynamodb=None):
    table = data.Table('subscription')
    response = table.get_item(
        Key={
        'email': email,
        'password':password
        }
    )
    
    if 'Item' in response:
        subscribed_music_old = response['Item'].get('songs', [])
        if subscribed_music_old:
            for music in subscribed_music:
                if music in subscribed_music_old:
                    subscribed_music_old.remove(music)
            response = table.update_item(
                Key={'email': email, 'password': password},
                UpdateExpression='SET songs = :val',
                ExpressionAttributeValues={':val': subscribed_music_old}
            )
            print(f"Successfully updated subscription for {email}")
    else:
        print(f"No subscription found for {email}")

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response