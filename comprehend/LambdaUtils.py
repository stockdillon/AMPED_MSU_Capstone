import boto3
import os
from amazon.api import AmazonAPI
import json
import Process
import aws_wrapper as aws
import requests
import itertools
import ItemWrapper
from pprint import pprint

JOBS_ENDPOINT = "http://api.amped.cc/api/jobs/"
TRANSCRIBE_JOBS_ENDPOINT = "http://api.amped.cc/api/jobs/?step=TRANSCRIBE"
MAX_ITEMS = 5

class LambdaUtils(object):
    """
    Handles interactions with API
    """
    def __init__(self,api_auth={"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}):
        self.client = aws.AWSClient()
        self.processor = Process.Processor(self.client)
        self.api_auth = api_auth
        self.jobs_endpoint = JOBS_ENDPOINT
        self.transcribe_jobs_endpoint = TRANSCRIBE_JOBS_ENDPOINT
        self.job_names_to_comprehend = self.get_job_names_to_comprehend()
        

    def get_item_set(self,job_name):
        """Gets a set of items related to a particular Transcribe job.
        
        Pulls transcription result from AWS console and extracts the text transcript. 
        Processes the text body to get relevant items from Amazon Marketplace, and extracts timestamps.
        Returns a list of the items with the key phrase used and timestamps.

        Returns:
            A list of named tuples, each of which containing a key phrase, a list of items from Amazon Marketplace,
        and a list of timestamps of when the keyphrase was mentioned in the audio file.
        """
        job_endpoint = "{}{}/".format(self.jobs_endpoint,str(job_name))
        result = requests.get(job_endpoint, headers=self.api_auth)
        job_json = result.json()
        job_category = job_json['category']
        print("Found category (SearchIndex): ", job_category)

        recent_job = self.client.transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name)
        transcribe_result_url = recent_job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcribe_response = requests.get(transcribe_result_url)
        transcribe_json_string = transcribe_response.content.decode('utf8')
        transcribe_json = json.loads(transcribe_json_string)
        #TODO move the above 5 lines into function get_transcript_text
        transcript_text = self.get_transcript_text(job_name)
        #print(transcript_text)

        items = self.processor.process(category=job_category, text=transcript_text)
        self.processor.extract_timestamps(transcribe_dicts=transcribe_json['results']['items'],items=items)

        return items


    def post_item_sets_all_jobs(self):
        """Posts results of ItemSearch to our Django framework API endpoint.

        Builds a dictionary containing all relevant information 
        for products related to a particular Transcribe job.
        This dictionary uses key phrases (search terms) for keys, 
        and maps each to a list of items and a list of timestamps for this key phrase.
        For each key phrase which has been determined to be significantly relevant, 
        we extract relevant attributes from the associated items

        """ 
        
        for job_name in self.job_names_to_comprehend:
            items = self.get_item_set(job_name)
            assert items, "No items were returned"
            #post_item_set(items, job_name)
            self.post_item_set(items, job_name)


    def post_item_set(self, kw_items_pairs, job_name):
        """
        Arguments:
        kw_items_pair: a list of named tuples with parameters keyword and a list of items
        """
        new_item_set = []
        for kw_items in kw_items_pairs:

            if not kw_items.timestamps:
                continue

            key_phrase_result = {}
            key_phrase_result['key_phrase'] = kw_items.keyword
            #key_phrase_result['items'] = []
            key_phrase_result['items'] = [ItemWrapper.ItemWebData(item).dict for item in list(itertools.islice(kw_items.items, 5)) if self.is_relevant(item)]
            key_phrase_result['timestamps'] = kw_items.timestamps

            """
            items = list(itertools.islice(kw_items.items, 5))
            wrapped_items = [ItemWrapper.ItemWebData(item) for item in items]

            for wrapped_item in wrapped_items:
                key_phrase_result['items'].append(wrapped_item.dict)
            """

            new_item_set.append(key_phrase_result)

        payload = {"products": json.dumps(new_item_set), "step": "FINISHED"}

        pprint("Payload: ")
        pprint(payload)

        response = requests.put(
            "{}{}/".format(self.jobs_endpoint, job_name), data=payload, headers=self.api_auth)

        print("Status code for put request: {} (LambdaUtils.post_item_set())".format(
            str(response.status_code)))

	

    def get_job_names_to_comprehend(self):
        """Gets the names of all jobs which are currently being Transcribed or waiting to be passed to AWS Comprehend.

        Retrieves the names of jobs which are currently waiting to be passed to AWS Comprehend
        from Django framework API endpoint. For each of these jobs, we check the AWS console to see if they
        have finished Transcribing. If the Transcribe job is complete, we add the name of the job to the list.

        Returns:
            A list of job names which are generated using a salted hash. For example:
            ['9c348223-5917-4700-b135-83135c9a927f', 
            '097c10d9-cb1f-439b-a90e-60da4afe4280', 
            'be4c2053-ee2d-4675-8caf-f4f7d308292d']
        """
        jobs_to_comprehend_response = requests.get(
            self.transcribe_jobs_endpoint, headers=self.api_auth)
        jobs_to_comprehend_list = jobs_to_comprehend_response.json()

        job_names_to_comprehend = []
        for job_object in jobs_to_comprehend_list:
            try:
                job_name = job_object['job_id']
                status = self.client.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name)['TranscriptionJob']['TranscriptionJobStatus']
                if(status == "COMPLETED"):
                    job_names_to_comprehend.append(job_name)
                else:
                    print("Job {} is still in the process of transcribing speech to text.".format(job_name))
            except:
                print("Error in json formatting of job (LambdaUtils.get_job_names_to_comprehend()).")

        return job_names_to_comprehend



    def get_transcript_text(self, job_name):
        recent_job = self.client.transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name)

        transcribe_result_url = recent_job['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcribe_response = requests.get(transcribe_result_url)
        transcribe_json_string = transcribe_response.content.decode('utf8')
        transcribe_json = json.loads(transcribe_json_string)
        transcript_text = transcribe_json['results']['transcripts'][0]['transcript']

        return transcript_text


    def is_relevant(self, item):
        return True