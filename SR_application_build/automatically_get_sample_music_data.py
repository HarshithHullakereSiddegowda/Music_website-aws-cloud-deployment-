from decimal import Decimal
import json
import boto3



def load_music(music, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb'
    ) 
    
    table = dynamodb.Table('Music')
    for music_s in music:
        title = str(music_s['title'])
        artist=str(music_s['artist'])
        web_url=str(music_s['web_url'])
        year = str(music_s['year'])
        image_url=str(music_s['img_url'])

        print("Adding music:", year, title, artist, web_url, image_url)
        table.put_item(Item=music_s)

if __name__ == '__main__':
    with open("musicdata.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
        m=music_list['songs']
    load_music(m)