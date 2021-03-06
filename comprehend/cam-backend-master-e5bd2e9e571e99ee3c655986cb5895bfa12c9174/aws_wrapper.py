from __future__ import print_function
import time
import boto3
from amazon.api import AmazonAPI

class AWSClient(object):
    """
    """
    def __init__(self,region=None,access_key=None,secret_access_key=None,tag=None):
        self.region = 'us-east-1'
        self.root_access_key = 'AKIAJB4BJYPJKV5YACXQ'
        self.root_secret_access_key = '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'
        self.search_access_key = 'AKIAIS2HFIM7UBM2H5CA'
        self.search_secret_access_key = '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'
        self.associate_tag = "msucapstone0a-20"
        self.create_comprehend_client()
        self.create_search_client()


    def create_comprehend_client(self):
        """
        """
        self.comprehend_client = boto3.client('comprehend',
                          region_name=self.region,
                          aws_access_key_id=self.root_access_key,
                          aws_secret_access_key=self.root_secret_access_key
                          )
        
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
        pass

    def search_n(self, keywords, index,n):
        return self.search_client.search_n(n,Keywords=keywords, SearchIndex=index)

        
