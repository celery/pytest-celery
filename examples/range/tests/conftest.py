from __future__ import annotations

import requests
from packaging.version import parse as parse_version


def get_celery_versions(start_version: str, end_version: str) -> list[str]:
    url = "https://pypi.org/pypi/celery/json"
    response = requests.get(url)
    data = response.json()
    all_versions = data["releases"].keys()

    filtered_versions = [
        v
        for v in all_versions
        if (
            parse_version(start_version) <= parse_version(v) <= parse_version(end_version)
            and not parse_version(v).is_prerelease
        )
    ]

    return sorted(filtered_versions, key=parse_version)
