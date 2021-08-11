FROM python:3.7.11

COPY cloud_build/requirements.txt /tmp/

RUN curl -OL https://storage.googleapis.com/ml-app-demo/model.h5 && \
	pip install --no-cache-dir -r /tmp/requirements.txt