from __future__ import print_function
import time
import boto3
transcribe = boto3.client('transcribe',
                          region_name='us-east-1',
                          aws_access_key_id='AKIAJB4BJYPJKV5YACXQ',
                          aws_secret_access_key='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'
                          )
job_name = "test_bucket"
job_uri = "https://s3.amazonaws.com/transcribe-me/Patagonia.mp3"
transcribe.start_transcription_job(
    TranscriptionJobName=job_name,
    Media={'MediaFileUri': job_uri},
    MediaFormat='mp3',
    LanguageCode='en-US'
)
while True:
    status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
        break
    print("Not ready yet...")
    time.sleep(5)
    
print(status)
