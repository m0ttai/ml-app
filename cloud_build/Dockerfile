# FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest
FROM python:3.7.11

COPY requirements.txt /tmp/

RUN curl -OL https://storage.googleapis.com/yu1-ml-demo/model.h5 && \
	pip install --no-cache-dir -r /tmp/requirements.txt