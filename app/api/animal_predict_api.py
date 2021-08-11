import io, os
import json
from flask import Flask, jsonify, request
from PIL import Image
import glob
from google.cloud.storage import bucket, client
import numpy as np
import tensorflow as tf
from google.cloud import storage as gcs
from google.oauth2 import service_account

listen_ip = os.environ['POD_IP_ADDRESS']
app = Flask(__name__)

@app.route('/', methods=['POST'])
def return_predict():
	# Variables
	gcs_project_id = 'direct-plateau-322502'
	gcs_key_path = '/config/direct-plateau-322502-d65283bd305e.json'
	gcs_bucket_name = 'yu1-ml-demo'
	class_label = ('cat', 'crow', 'horse', 'lion', 'turtle')
	model_path = '/model.h5'
	model = tf.keras.models.load_model(model_path)
	X = []

	# Get Request
	req = json.loads(request.json)

	# Get Image File
	gcs_client = gcs.Client(gcs_project_id, credentials=service_account.Credentials.from_service_account_file(gcs_key_path))
	gcs_bucket = gcs_client.get_bucket(gcs_bucket_name)
	predict_file = gcs_bucket.get_blob(req['file_name'])

	# Retouch & Convert Image File
	input_file = Image.open(io.BytesIO(predict_file.download_as_string()))
	input_file = input_file.convert('RGB')
	input_file = input_file.resize((100, 100))
	input_file = np.asarray(input_file)
	X.append(input_file)
	X = np.array(X)

	# Predict Image File
	results = model.predict([X])[0]

	# Set Object's Metadata
	gcs_metadata = {'class': class_label[results.argmax()]}
	predict_file.metadata = gcs_metadata
	predict_file.patch()
	return jsonify({"message": "{} is {}".format(predict_file.name, predict_file.metadata)})

if __name__ == '__main__':
	app.run(host=listen_ip, port=80, debug=True)