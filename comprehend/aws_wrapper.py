from __future__ import print_function
import time
import boto3
from amazon.api import AmazonAPI

class AWSClient(object):
    """
    """
    def __init__(self,region=None,root_access_key='AKIAJB4BJYPJKV5YACXQ',
                                  root_secret_access_key='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',tag=None):

        self.region = 'us-east-1'
        self.root_access_key = root_access_key
        self.root_secret_access_key = root_secret_access_key
        self.search_access_key = 'AKIAIMJ3KXAGVLAEFBNA' #affiliate key
        self.search_secret_access_key = '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' #affiliate key
        self.associate_tag = "msucapstone02-20"
        self.create_comprehend_client()
        self.create_search_client()
        self.create_transcribe_client()


    def create_client(self,service):
        """
        """
        return boto3.client(service,
                  region_name=self.region,
                  aws_access_key_id=self.root_access_key,
                  aws_secret_access_key=self.root_secret_access_key
                  )

    def create_transcribe_client(self):
        """
        """
        self.transcribe_client = self.create_client('transcribe')

    def create_comprehend_client(self):
        """
        """
        self.comprehend_client = self.create_client('comprehend')
        
    def create_search_client(self):
        self.search_client = AmazonAPI(self.search_access_key,
                                       self.search_secret_access_key,
                                       self.associate_tag)
        
    def run_transcribe_job(self):
        pass

    def comprehend_entities(self,text_input):
        response = self.comprehend_client.detect_entities(
        Text=text_input,
        LanguageCode='en'
        )

        return response

    def comprehend_key_phrases(self,text_input):
        response = self.comprehend_client.detect_key_phrases(
        Text=text_input,
        LanguageCode='en'
        )

        return response

    def comprehend_sentiment(self,text_input):
        response = self.comprehend_client.detect_sentiment(
            Text=text_input,
            LanguageCode='en'
        )
        
        return response

    def search_n(self, keywords, index,n):
        return self.search_client.search_n(n, Keywords=keywords, SearchIndex=index)

        
