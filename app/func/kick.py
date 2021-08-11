import requests
import json
import os

def request_metadata():
	### Variables ###
	host = os.environ['POD_IP_ADDRESS']
	port = '80'
	url = 'http://' + host + ':' + port + '/'
	# url = 'http://35.187.223.154:10080/'
	print(url)
	payload = {"file_name": "cat.jpg"}

	# Send request
	res = requests.post(url, json=json.dumps(payload))

	# Logging
	print('Response Headers: ', res.headers)
	print('Response Body: ', res.text)

	return

if __name__ == '__main__':
	request_metadata()