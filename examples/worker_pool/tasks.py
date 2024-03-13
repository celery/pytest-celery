# Based on https://github.com/celery/celery/blob/main/examples/gevent/tasks.py

import requests
from celery import shared_task


@shared_task(ignore_result=True)
def urlopen(url):
    print(f"Opening: {url}")
    try:
        requests.get(url)
    except requests.exceptions.RequestException as exc:
        print(f"Exception for {url}: {exc!r}")
        return url, 0
    print(f"Done with: {url}")
    return url, 1
