import get_details
import boto3
import os
import aws_properties as AWS
import subprocess
import botocore
import shutil
import eval_face_recognition

AWS_ACCESS_KEY_ID = AWS.AWS_SERVER_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = AWS.AWS_SERVER_SECRET_KEY
INPUT_BUCKET = AWS.INPUT_BUCKET_NAME
REGION_NAME = AWS.REGION_NAME
OUTPUT_BUCKET = AWS.OUTPUT_BUCKET_NAME


s3_client = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key= AWS_SECRET_ACCESS_KEY,region_name=REGION_NAME)
s3_resource = boto3.resource('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key= AWS_SECRET_ACCESS_KEY,region_name=REGION_NAME)


# List all objects within a S3 bucket path
def download_file(filename):
    try:
        path = '/tmp/'
        video_path = os.path.join(path,filename)
        s3_resource.Bucket(INPUT_BUCKET).download_file(filename,video_path)
        return video_path 
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def process(frames_path,key_name):
    path = '/tmp/'
    list_of_results = []
    for filename in os.listdir(frames_path):
        print(filename)
        p = eval_face_recognition.eval(os.path.join(frames_path,filename))
        k = str(p)
        print(k)
        result = k.split(',')[1].split(')')[0].strip()
        list_of_results.append(result)
    info = {'listofnames':list_of_results,'keyname':key_name}
    response = get_details.get_details(info)
    shutil.rmtree(frames_path)
    if(response['ResponseMetadata']['HTTPStatusCode']==200):
        return {"result":"File uploaded to S3 sucessfully"}

    

def handler(event,context):
    filename=event['Records'][0]['s3']['object']['key']
    video_file_path = download_file(filename)
    print(os.listdir('/tmp'))
    path = '/tmp/'
    print(path)
    key_name = filename.split('.')[0]
    frames_path = os.path.join(path,key_name)
    if(not os.path.isdir(frames_path)):
        os.mkdir(frames_path)
    os.system("ffmpeg -i " + str(video_file_path) +" -vf fps=2 "+ str(frames_path)+'/' + key_name+"-%3d.jpeg")
    os.remove(video_file_path)
    print(frames_path)
    result = process(frames_path,key_name)
    return result