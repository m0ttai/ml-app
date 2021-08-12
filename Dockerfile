FROM python:3.7.11

COPY requirements.txt /tmp/

RUN pip install --no-cache-dir -r /tmp/requirements.txt
