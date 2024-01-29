import logging
import boto3
from botocore.exceptions import ClientError 
import urllib.request
from decimal import Decimal
import json


# def upload_file(file_name, bucket, object_name=None):
#     """Upload a file to an S3 bucket
#     :param file_name: File to upload
#     :param bucket: Bucket to upload to
#     :param object_name: S3 object name. If not specified then file_name is
#     used
#     :return: True if file was uploaded, else False
#     """
# # If S3 object_name was not specified, use file_name
#     if object_name is None:
#         object_name = file_name
#     # Upload the file
# #create an s3 client   
#     s3_client = boto3.client('s3')
#     try:
#         response = s3_client.upload_file(file_name, bucket, object_name)
#     except ClientError as e:
#         logging.error(e)
#     return False

#     return True

# s3 = boto3.client('s3')
# with open("musicdata.json", "rb") as final:
#     s3.upload_fileobj(final, "BUCKET_NAME", "OBJECT_NAME")



import logging
import boto3
from botocore.exceptions import ClientError 
import requests
import os

#def  load_music(music, bucket, object_name=None):
def  load_music(music):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is
    used
    :return: True if file was uploaded, else False
    """

    temp_dir=("temp4")


    # temp_dir=os.path.abspath("temp4")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for artists in music:
        
        img_url= artists.get("img_url")

        
        # print(img_url)
        if img_url:
            response= requests.get(img_url)
            # print(response)
            if response.status_code==200:
                filename= os.path.join(temp_dir, f"{artists.get('artist')}.jpg")
                with open(filename, "wb") as file:
                    file.write(response.content)

                    file_str=str(file.name) 



                    print(file_str)


   

if __name__ == '__main__':
    with open("musicdata.json") as json_file:
        music_list = json.load(json_file, parse_float=Decimal)
        m=music_list['songs']
    load_music(m)