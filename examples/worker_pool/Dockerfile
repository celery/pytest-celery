FROM python:3.11-bookworm

# Create a user to run the worker
RUN adduser --disabled-password --gecos "" test_user

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential git libevent-dev

# Set arguments
ARG CELERY_LOG_LEVEL=INFO
ARG CELERY_WORKER_NAME=my_worker
ARG CELERY_WORKER_QUEUE=celery
ENV LOG_LEVEL=$CELERY_LOG_LEVEL
ENV WORKER_NAME=$CELERY_WORKER_NAME
ENV WORKER_QUEUE=$CELERY_WORKER_QUEUE

# Install packages
COPY --chown=test_user:test_user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r ./requirements.txt

# The workdir must be /app
WORKDIR /app

# Switch to the test_user
USER test_user

# Start the celery worker
CMD celery -A app worker --loglevel=$LOG_LEVEL -n $WORKER_NAME@%h -Q $WORKER_QUEUE
