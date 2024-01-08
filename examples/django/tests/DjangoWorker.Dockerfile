FROM python:3.11-bookworm

# Create a user to run the worker
RUN adduser --disabled-password --gecos "" test_user

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Set arguments
ARG CELERY_LOG_LEVEL=INFO
ARG CELERY_WORKER_NAME=celery_dev_worker
ARG CELERY_WORKER_QUEUE=celery
ENV LOG_LEVEL=$CELERY_LOG_LEVEL
ENV WORKER_NAME=$CELERY_WORKER_NAME
ENV WORKER_QUEUE=$CELERY_WORKER_QUEUE

# Install packages
WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r ./requirements.txt

# Switch to the test_user
USER test_user

# Start the celery worker
CMD celery -A proj worker --loglevel=$LOG_LEVEL -n $WORKER_NAME@%h -Q $WORKER_QUEUE
