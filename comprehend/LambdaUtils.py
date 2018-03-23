import boto3
import os
from amazon.api import AmazonAPI
import json
import Process
import aws_wrapper as aws
import requests

class LambdaUtils(object):
    """
    Handles interactions with API
    """
    def __init__(self,api_auth={"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}):
        self.client = aws.AWSClient()
        self.api_auth = api_auth
        

    def get_item_set(self,jobName):
        """
        """
        jobEndpoint = "http://api.amped.cc/api/jobs/" + str(jobName) + "/"
        result = requests.get(jobEndpoint, headers=self.api_auth)
        jobJSON = result.json()
        #jobStatus = jobJSON['step']
        jobCategory = jobJSON['category']
        print("Found category (SearchIndex): ", jobCategory)
        #print("Status of job {}: {}".format(jobName, jobStatus))

        recentJob = self.client.transcribe_client.get_transcription_job(TranscriptionJobName=jobName)

        transcribe_result_URL = recentJob['TranscriptionJob']['Transcript']['TranscriptFileUri']
        transcribe_response = requests.get(transcribe_result_URL)
        transcribe_JSON_string = transcribe_response.content.decode('utf8')
        transcribe_JSON = json.loads(transcribe_JSON_string)

        text = transcribe_JSON['results']['transcripts'][0]['transcript']
        #print(text)

        processor = Process.Processor(self.client)
        #items = processor.process(category="Electronics",text=text)
        items = processor.process(category=jobCategory,text=text)
        processor.extract_timestamps(transcribe_dicts=transcribe_JSON['results']['items'],items=items)

        return items


    def post_item_sets_all_jobs(self):
        """
        """

        def post_item_set(kw_items_pairs, jobName):
            """
            Arguments:
            kw_items_pair: a list of named tuples with parameters keyword and a list of items
            """		
            newItemSet = {}
            for kw_items in kw_items_pairs:

                newItemSet[kw_items.keyword] = []

                for i, item in enumerate(kw_items.items):
                    if i > 5:
                        break
                    itemData = {}
                    try:
                        print(item.title)
                        itemData['title'] = str(item.title)
                        itemData['price'] = str(item.formatted_price)
                        itemData['brand'] = str(item.brand)
                        itemData['asin'] = str(item.asin)
                        itemData['url'] = str(item.offer_url)
                        itemData['image_url'] = str(item.images[0].LargeImage.URL)
                        itemData['description'] = str(item.editorial_review)
                        itemData['images'] = list(set(map(lambda _: str(_.LargeImage.URL), item.images)))
                        itemData['timestamps'] = kw_items.timestamps
                    except:
                        pass
                    newItemSet[kw_items.keyword].append(itemData)


            payload = {"products" : json.dumps(newItemSet), "step": "FINISHED"}

            print("Payload: ", payload)

            #headers = {"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}
            result = requests.put("http://api.amped.cc/api/jobs/" + jobName + "/", data=payload, headers=self.api_auth)
            print("Status code for put request: " + str(result.status_code))
        
        
        print("Getting jobs not comprehended...")
        jobNames = self.get_completed_jobs_not_comprehended()
        print(jobNames)
        for jobName in jobNames:
            items = self.get_item_set(jobName)
            assert items, "No items were returned"
            post_item_set(items, jobName)




    def get_completed_jobs_not_comprehended(self):
        jobEndpoint = "http://api.amped.cc/api/jobs/?step=TRANSCRIBE"
        result = requests.get(jobEndpoint, headers=self.api_auth)
        jobs = result.json()

        completedJobsNotComprehendedNames = []
        for job in jobs:
            try:
                jobName = job['job_id']
                status = self.client.transcribe_client.get_transcription_job(TranscriptionJobName=jobName)['TranscriptionJob']['TranscriptionJobStatus']
                #print("job_id: " + job['job_id'] + "| Status:" + status)
                if(status == "COMPLETED"):
                    completedJobsNotComprehendedNames.append(jobName)
            except:
                pass

        return completedJobsNotComprehendedNames
	
