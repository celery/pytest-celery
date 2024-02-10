"""The pytest-celery plugin provides a set of built-in components called
:ref:`vendors`.

This module is part of the :ref:`built-in-worker` vendor.
"""

from __future__ import annotations

import json

import psutil


def get_running_processes_info(columns: list[str] | None = None) -> str:
    """Get information about running processes using psutil."""
    if not columns:
        columns = [
            "pid",
            "name",
            "username",
            "cmdline",
            "cpu_percent",
            "memory_percent",
            "create_time",
        ]
    processes = [proc.info for proc in psutil.process_iter(columns)]
    return json.dumps(processes)
