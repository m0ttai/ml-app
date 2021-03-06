### Libraries ###
import io, os
import json
from flask import Flask, jsonify, request
from PIL import Image
import numpy as np
import tensorflow as tf
from google.cloud import storage as gcs
from google.oauth2 import service_account

listen_ip = os.environ['POD_IP_ADDRESS']
app = Flask(__name__)

### Authenticate Google Cloud Storage & Download the Model ###
gcs_project_id = os.environ['GC_PROJECT_ID']
gcs_key_path = '/config/gcs_key.json'
gcs_bucket_name = os.environ['GCS_BUCKET_NAME']
gcs_client = gcs.Client(gcs_project_id, credentials=service_account.Credentials.from_service_account_file(gcs_key_path))
gcs_bucket = gcs_client.get_bucket(gcs_bucket_name)
model_path = '/model.h5'
ml_model = gcs_bucket.blob('model.h5')
ml_model.download_to_filename(model_path)

@app.route('/', methods=['POST'])
def return_predict():
	### Variables ###
	class_label = ('cat', 'crow', 'horse', 'lion', 'turtle')
	model = tf.keras.models.load_model(model_path)
	X = []

	### Get Request ###
	req = json.loads(request.json)

	### Get Image File from GCS ###
	predict_file = gcs_bucket.get_blob(req['file_name'])

	### Retouch & Convert Image File ###
	input_file = Image.open(io.BytesIO(predict_file.download_as_string()))
	input_file = input_file.convert('RGB')
	input_file = input_file.resize((100, 100))
	input_file = np.asarray(input_file)
	X.append(input_file)
	X = np.array(X)

	### Predict Image File ###
	results = model.predict([X])[0]

	### Set Object's Metadata ###
	gcs_metadata = {'class': class_label[results.argmax()]}
	predict_file.metadata = gcs_metadata
	predict_file.patch()
	return jsonify({"message": "{} is {}".format(predict_file.name, predict_file.metadata)})

if __name__ == '__main__':
	app.run(host=listen_ip, port=80)
