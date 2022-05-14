import aws_properties as AWS
import boto3
import os
from boto3.dynamodb.conditions import Key

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
REGION_NAME = AWS.REGION_NAME
TABLENAME = AWS.TABLENAME
RESULT_BUCKET = AWS.RESULT_BUCKET_NAME

dynamodb = boto3.resource('dynamodb',region_name=REGION_NAME,aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key=AWS_SERVER_SECRET_KEY)
table = dynamodb.Table(TABLENAME)
s3_client = boto3.client('s3',aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key= AWS_SERVER_SECRET_KEY,region_name=REGION_NAME)
s3_resource = boto3.resource('s3',aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key= AWS_SERVER_SECRET_KEY,region_name=REGION_NAME)

def upload_file(filename):
    file_path = '/tmp/'
    response = s3_resource.Object(RESULT_BUCKET, filename).put(Body=open(os.path.join(file_path,filename), 'rb'))

    return response

def get_details(info):

    key_name = info['keyname']
    list_of_results = info['listofnames']
    path = '/tmp/'
    my_file = open(os.path.join(path,key_name+".txt"), "w")
    for item in list_of_results:
        item_number = key_name
        response=table.get_item(Key={'name':item.capitalize()})
        my_file.write(str(item_number)+': '+response['Item']['name']+', '+response['Item']['major']+', '+response['Item']['year']+'\n')
    my_file.close()
    response = upload_file(key_name+'.txt')
    return response
