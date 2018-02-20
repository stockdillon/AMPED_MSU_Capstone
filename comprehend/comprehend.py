import boto3
import os
import requests
from amazon.api import AmazonAPI
import json
import Process
import aws_wrapper as aws

AWS_WRAPPER = aws.AWSClient()

def lambda_handler(event, context):
	print("STARTING JOB")
	transcribe_client = AWS_WRAPPER.transcribe_client

	jobNames = Get_Completed_Jobs_Not_Comprehended(transcribe_client)
	for jobName in jobNames:
		items = GetItemSet(jobName,transcribe_client)
		print("Job Name: ", jobName, "Items: ", items)
		assert items, "No items were returned"
		result = PostItemSet(items, jobName)

		#debugging#
		#print("Result of " + jobName + ": ")
		#print(items)

	print("Success!!!")
	return {
	    'isValid': True,
	    'message': {'contentType': 'PlainText', 'content': "hacked"}
	}





def GetItemSet(jobName,transcribe_client):
	"""
	"""

	headers = {"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}
	jobEndpoint = "http://api.amped.cc/api/jobs/" + str(jobName) + "/"
	result = requests.get(jobEndpoint, headers=headers)
	jobStatus = result.json()['step']
	print("Status of job {}: {}".format(jobName, jobStatus))


	recentJob = transcribe_client.get_transcription_job(TranscriptionJobName=jobName)


	result_URL = recentJob['TranscriptionJob']['Transcript']['TranscriptFileUri']
	response = requests.get(result_URL)
	jsonString = response.content.decode('utf8')
	loadJSON = json.loads(jsonString)
	print(loadJSON['results']['transcripts'][0]['transcript'])


	text = loadJSON['results']['transcripts'][0]['transcript']

	processor = Process.Processor()
	items = processor.process(category="Electronics",text=text)

	return items


def PostItemSet(kw_items_pairs, jobName):
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
			except:
				pass
			newItemSet[kw_items.keyword].append(itemData)


	payload = {"products" : json.dumps(newItemSet), "step": "FINISHED"}

	#print("Payload: ", payload)

	headers = {"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}
	result = requests.put("http://api.amped.cc/api/jobs/" + jobName + "/", data=payload, headers=headers)
	print("Status code for put request: " + str(result.status_code))
	#print(newItemSet)
	return newItemSet





def Get_Completed_Jobs_Not_Comprehended(transcribe):
	headers = {"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}
	jobEndpoint = "http://api.amped.cc/api/jobs/?step=TRANSCRIBE"
	result = requests.get(jobEndpoint, headers=headers)
	jobs = result.json()

	completedJobsNotComprehendedNames = []
	for job in jobs:
		try:
			jobName = job['job_id']
			status = transcribe.get_transcription_job(TranscriptionJobName=jobName)['TranscriptionJob']['TranscriptionJobStatus']
			#print("job_id: " + job['job_id'] + "| Status:" + status)
			if(status == "COMPLETED"):
				completedJobsNotComprehendedNames.append(jobName)
		except:
			pass

	###############################################################################
	"""
	jobs = transcribe.list_transcription_jobs(Status="COMPLETED", MaxResults=10)
	completedJobsNotComprehendedNames = []

	done = False
	while(not done):
		currentPageJobNames = [summary['TranscriptionJobName'] for summary in jobs['TranscriptionJobSummaries']]

		for jobName in currentPageJobNames:
			# Check API for the status of the job. If the job is status is 'TRANSCRIBE', we need to Comprehend it
			# else, we are done collecting jobs. (break)
			status = Get_API_Job_Status(jobName)
			if(status != "TRANSCRIBE"):
				done = True
				break

			else:
				completedJobsNotComprehendedNames.append(jobName)

		jobs = transcribe.list_transcription_jobs(Status = "COMPLETED", MaxResults=10, NextToken=jobs['NextToken'])
	"""
	###############################################################################

	return completedJobsNotComprehendedNames
	



def Get_API_Job_Status(jobName):
	headers = {"Authorization":"Token 764aab954fdc86cadb3b4cbd2b9f6f48339e6566"}
	jobEndpoint = "http://api.amped.cc/api/jobs/" + str(jobName) + "/"
	result = requests.get(jobEndpoint, headers=headers)

	#print(jobName)
	status = result.json()['step']

	print("Job Name: " + jobName + " has status: " + status)

	return status


















