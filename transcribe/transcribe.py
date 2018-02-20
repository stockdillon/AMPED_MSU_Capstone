import boto3
import os
import requests

def lambda_handler(event, context):
    transcribe = boto3.client('transcribe',
                         region_name='us-east-1',
                         aws_secret_access_key="YIaeWyQPhwwXUI2zKtpIs50p+w80wnPrz22YRF7q",
                         aws_access_key_id="AKIAJB4BJYPJKV5YACXQ")
    
    
    job_id = event['queryStringParameters']['job_id']
    job_uri = event['queryStringParameters']['job_uri']

    filepath, extension = os.path.splitext(job_uri)
    extension = extension.strip('.')

    transcribe.start_transcription_job(
       TranscriptionJobName=job_id,
       Media={'MediaFileUri': job_uri},
       MediaFormat=extension,
       LanguageCode='en-US'
    )

    print("job_id: ", job_id)
    print("job_uri: ", job_uri)


    print("Success!!!")
    return {
        'isValid': True,
        'message': {'contentType': 'PlainText', 'content': "hacked"}
    }