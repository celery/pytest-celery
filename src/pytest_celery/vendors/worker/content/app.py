"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`. This module is part of the :ref:`built-in-worker` vendor.

Template for Celery worker application.
"""

from __future__ import annotations

import json

from celery import Celery

imports = None

app = Celery("celery_test_app")
config = None

if config:
    app.config_from_object(config)
    print(f"Changed worker configuration: {json.dumps(config, indent=4)}")


if __name__ == "__main__":
    app.start()
