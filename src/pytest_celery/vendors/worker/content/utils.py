import json

import psutil


def get_running_processes_info(columns: list[str] | None = None) -> str:
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
