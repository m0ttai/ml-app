import requests
import json

def request_metadata(data, context):
	# Variables
	url = 'http://34.84.140.203:10080/'
	target = data['name']
	payload = {"file_name": target}

	# Send request
	res = requests.post(url, json=json.dumps(payload))

	# Logging
	print('Payload: ', payload)
	print('Response Headers: ', res.headers)
	print('Response Body: ', res.text)

	return