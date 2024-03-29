FROM python:3.10-slim-buster

# Create a user to run the worker
RUN adduser --disabled-password --gecos "" test_user

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential git

# Set arguments
ARG CELERY_VERSION=""
ARG CELERY_LOG_LEVEL=INFO
ARG CELERY_WORKER_NAME=celery_test_worker
ARG CELERY_WORKER_QUEUE=celery
ENV WORKER_VERSION=$CELERY_VERSION
ENV LOG_LEVEL=$CELERY_LOG_LEVEL
ENV WORKER_NAME=$CELERY_WORKER_NAME
ENV WORKER_QUEUE=$CELERY_WORKER_QUEUE

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade \
    pip \
    celery[redis,pymemcache]${WORKER_VERSION:+==$WORKER_VERSION} \
    pytest-celery@git+https://github.com/celery/pytest-celery.git

# The workdir must be /app
WORKDIR /app

COPY content/ .

# Switch to the test_user
USER test_user

# Start the celery worker
CMD celery -A app worker --loglevel=$LOG_LEVEL -n $WORKER_NAME@%h -Q $WORKER_QUEUE
