import boto3
from properties import aws_properties as AWS
import os
import botocore

AWS_SERVER_ACCESS_KEY = AWS.AWS_SERVER_ACCESS_KEY
AWS_SERVER_SECRET_KEY = AWS.AWS_SERVER_SECRET_KEY
INPUT_BUCKET_NAME = AWS.INPUT_BUCKET_NAME
RESULT_BUCKET = AWS.RESULTS_BUCKET_NAME
REGION_NAME = AWS.REGION_NAME

s3 = boto3.client('s3', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key = AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)
s3_resource = boto3.resource('s3', aws_access_key_id=AWS_SERVER_ACCESS_KEY,aws_secret_access_key = AWS_SERVER_SECRET_KEY, region_name=REGION_NAME)

def upload_to_s3(filepath):
    
    filename = filepath.split('/')[4]
    s3.upload_file(Filename=filepath, Bucket=INPUT_BUCKET_NAME, Key=filename)
    os.remove(filepath)

def retreive_results(filename):

    filename = filename.split('.')[0]
    filename = filename+'.txt'
    
    while True:
       try:
           s3_resource.Bucket(RESULT_BUCKET).download_file(filename,filename)
       except Exception as e:
           pass
       path = os.path.dirname(__file__)
       if(os.path.exists(os.path.join(path,filename))):
           break

    f = open(filename,"r")
    l = f.readlines()
    return l

    