import LambdaUtils

def lambda_handler(event, context):
	print("STARTING JOB")
	
	lambda_utils = LambdaUtils.LambdaUtils()
	lambda_utils.post_item_sets_all_jobs()

	return {
	    'isValid': True,
	    'message': {'contentType': 'PlainText', 'content': "hacked"}
	}
