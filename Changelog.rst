.. _changelog:

================
 Change history
================

.. _version-1.1.2:

1.1.2
=====
:release-date: 14 August, 2024
:release-by: Tomer Nosrati

What's Changed
==============

Key Highlights
--------------

Fixed Redis container instabilities in #405

Other Changes
-------------
- Build(deps): Bump botocore from 1.34.158 to 1.34.161 (#382)
- Build(deps): Bump boto3 from 1.34.158 to 1.34.161 (#383)
- Build(deps): Bump botocore from 1.34.161 to 1.34.162 (#384)
- Build(deps): Bump setuptools from 72.1.0 to 72.2.0 (#381)
- Build(deps-dev): Bump types-redis from 4.6.0.20240806 to 4.6.0.20240819 (#385)
- Build(deps): Bump boto3 from 1.34.161 to 1.34.162 (#386)
- Build(deps): Bump setuptools from 72.2.0 to 73.0.0 (#387)
- Build(deps): Bump setuptools from 73.0.0 to 73.0.1 (#388)
- Build(deps-dev): Bump mypy from 1.11.1 to 1.11.2 (#389)
- Build(deps): Bump setuptools from 73.0.1 to 74.0.0 (#390)
- Build(deps): Bump urllib3 from 1.26.19 to 1.26.20 (#391)
- Build(deps): Bump setuptools from 74.0.0 to 74.1.0 (#392)
- Build(deps-dev): Bump types-redis from 4.6.0.20240819 to 4.6.0.20240903 (#393)
- Build(deps): Bump setuptools from 74.1.0 to 74.1.1 (#394)
- Build(deps): Bump setuptools from 74.1.1 to 74.1.2 (#395)
- Added docker cleanup auto-fixture to improve tests stability (#396)
- Changed --reruns 3 -> 5 in the CI for hybrid_setup example (to mitigate docker failures) (#398)
- Added "--reruns-delay 10" in the examples CI (#399)
- Bumping Dependencies (inc. pyproject.toml) (#397)
- Build(deps-dev): Bump pytest from 8.3.2 to 8.3.3 (#402)
- blacksmith.sh: Migrate workflows to Blacksmith (#403)
- Build(deps): Bump botocore from 1.35.14 to 1.35.18 (#404)
- Fix Redis container from aborting randomly (#405)
- Prepare for release: v1.1.2 (#406)

.. _version-1.1.1:

1.1.1
=====
:release-date: 12 August, 2024
:release-by: Tomer Nosrati

What's Changed
==============

- Added installation markers for pycurl (#378)
- Changed --reruns 3 -> 5 for Integration and Smoke CI (#380)
- Prepare for release: v1.1.1 (#379)

.. _version-1.1.0:

1.1.0
=====
:release-date: 11 August, 2024
:release-by: Tomer Nosrati

What's Changed
==============

Key Highlights
--------------

- New SQS broker using :ref:`Localstack <built-in-localstack-broker>` (Disabled by default).
- New ``sqs`` extra for the SQS broker.

Fixes & Changes
---------------

- Fixed package docutils installation with Python 3.8 (#372)
- Added sqs extra (only) (#373)
- Use set instead of list with ALL_CELERY_BROKERS and ALL_CELERY_BACKENDS (#375)
- Added new localstack (SQS) broker (#374)
- Prepare for release: v1.1.0 (#377)

Dependencies Updates
--------------------

- Build(deps): Bump setuptools from 70.3.0 to 71.0.3 (#354)
- Bumping Dependencies (inc. pyproject.toml) (#355)
- Build(deps-dev): Bump pytest from 8.3.1 to 8.3.2 (#357)
- Build(deps): Bump setuptools from 71.1.0 to 72.1.0 (#360)
- Build(deps-dev): Bump types-redis from 4.6.0.20240425 to 4.6.0.20240726 (#356)
- Build(deps): Bump tenacity from 8.5.0 to 9.0.0 (#361)
- Build(deps): Bump redis from 5.0.7 to 5.0.8 (#362)
- Build(deps-dev): Bump mypy from 1.11.0 to 1.11.1 (#363)
- Build(deps): Bump snok/install-poetry from 1.3.4 to 1.4.0 (#364)
- Build(deps-dev): Bump coverage from 7.6.0 to 7.6.1 (#365)
- Build(deps): Bump debugpy from 1.8.2 to 1.8.3 (#366)
- Build(deps-dev): Bump black from 24.4.2 to 24.8.0 (#367)
- Build(deps): Bump snok/install-poetry from 1.4.0 to 1.4.1 (#368)
- Build(deps): Bump debugpy from 1.8.3 to 1.8.5 (#370)
- Build(deps-dev): Bump types-redis from 4.6.0.20240726 to 4.6.0.20240806 (#371)
- Bumping Dependencies (inc. pyproject.toml) (#376)

.. _version-1.0.1:

1.0.1
=====
:release-date: 17 July, 2024
:release-by: Tomer Nosrati

What's Changed
==============

Fixes & Changes
---------------

- Cleanup: pytest-celery[all]==1.0.0b4 -> pytest-celery[all]==1.0.0 (#330)
- Fixed hybrid_setup example build error with legacy.Dockerfile (#331)
- Fix typos (#339)
- Prepare for release: v1.0.1 (#351)
- Added changelog for v1.0.1 (#350)

Security Fixes
--------------

- `CVE-2024-39689 <https://github.com/advisories/GHSA-248v-346w-9cwc>`_: Certifi removes GLOBALTRUST root certificate
- `CVE-2024-3651 <https://github.com/advisories/GHSA-jjg7-2v4v-x38h>`_: Internationalized Domain Names in Applications (IDNA) vulnerable to denial of service from specially crafted inputs to idna.encode
- `CVE-2024-34064 <https://github.com/advisories/GHSA-h75v-3vvj-5mfj>`_: Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter
- `GHSA-753j-mpmx-qq6g <https://github.com/advisories/GHSA-753j-mpmx-qq6g>`_: Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') in tornado
- `GHSA-w235-7p84-xx57 <https://github.com/advisories/GHSA-w235-7p84-xx57>`_: Tornado has a CRLF injection in CurlAsyncHTTPClient headers
- `CVE-2024-37891 <https://github.com/advisories/GHSA-34jh-p97f-mpxf>`_: urllib3's Proxy-Authorization request header isn't stripped during cross-origin redirects
- `CVE-2024-5569 <https://github.com/advisories/GHSA-jfmj-5v4g-7637>`_: zipp Denial of Service vulnerability
- `CVE-2024-35195 <https://github.com/advisories/GHSA-9wx4-h78v-vm56>`_: Requests Session object does not verify requests after making first request with verify=False

Dependencies Updates
--------------------

- Build(deps-dev): Bump black from 24.3.0 to 24.4.0 (#289)
- Build(deps): Bump setuptools from 69.2.0 to 69.5.1 (#290)
- Build(deps-dev): Bump types-redis from 4.6.0.20240409 to 4.6.0.20240417 (#292)
- Build(deps): Bump celery from 5.3.6 to 5.4.0 (#293)
- Build(deps-dev): Bump types-redis from 4.6.0.20240417 to 4.6.0.20240423 (#295)
- Build(deps-dev): Bump coverage from 7.4.4 to 7.5.0 (#296)
- Build(deps-dev): Bump mypy from 1.9.0 to 1.10.0 (#298)
- Build(deps-dev): Bump black from 24.4.0 to 24.4.1 (#299)
- Build(deps-dev): Bump types-redis from 4.6.0.20240423 to 4.6.0.20240425 (#300)
- Build(deps): Bump redis from 5.0.3 to 5.0.4 (#297)
- Build(deps-dev): Bump black from 24.4.1 to 24.4.2 (#301)
- Build(deps-dev): Bump pytest from 8.1.1 to 8.2.0 (#302)
- Build(deps-dev): Bump pytest-xdist from 3.5.0 to 3.6.1 (#303)
- Build(deps-dev): Bump coverage from 7.5.0 to 7.5.1 (#306)
- Build(deps-dev): Bump sphinx-click from 5.1.0 to 6.0.0 (#308)
- Build(deps-dev): Bump pytest from 8.2.0 to 8.2.1 (#309)
- Revert "Build(deps-dev): Bump pytest from 8.2.0 to 8.2.1" (#310)
- Pinned requests to v2.31.0 due to docker-py bug #3256 (#313)
- Build(deps-dev): Bump pytest from 8.2.0 to 8.2.1 (#311)
- Build(deps): Bump setuptools from 69.5.1 to 70.0.0 (#312)
- Build(deps): Bump docker from 7.0.0 to 7.1.0 (#315)
- Fixed docker-py & requests issue (#316)
- Build(deps-dev): Bump coverage from 7.5.1 to 7.5.2 (#317)
- Build(deps-dev): Bump coverage from 7.5.2 to 7.5.3 (#319)
- Build(deps-dev): Bump pytest from 8.2.1 to 8.2.2 (#320)
- Build(deps): Bump redis from 5.0.4 to 5.0.5 (#321)
- Build(deps): Bump redis from 5.0.5 to 5.0.6 (#323)
- Build(deps): Bump psutil from 5.9.8 to 6.0.0 (#325)
- Build(deps): Bump setuptools from 70.0.0 to 70.1.0 (#327)
- Build(deps-dev): Bump coverage from 7.5.3 to 7.5.4 (#328)
- Build(deps-dev): Bump mypy from 1.10.0 to 1.10.1 (#329)
- Build(deps): Bump setuptools from 70.1.0 to 70.1.1 (#332)
- Build(deps): Bump debugpy from 1.8.1 to 1.8.2 (#333)
- Build(deps): Bump redis from 5.0.6 to 5.0.7 (#334)
- Build(deps): Bump setuptools from 70.1.1 to 70.2.0 (#336)
- Build(deps): Bump certifi from 2024.2.2 to 2024.7.4 (#337)
- Build(deps-dev): Bump pytest-subtests from 0.12.1 to 0.13.0 (#338)
- Build(deps): Bump setuptools from 70.2.0 to 70.3.0 (#340)
- Build(deps-dev): Bump coverage from 7.5.4 to 7.6.0 (#341)
- Changed "retry" dependency to "tenacity" (#342)
- Build(deps): Bump idna from 3.6 to 3.7 (#343)
- Build(deps-dev): Bump jinja2 from 3.1.3 to 3.1.4 (#344)
- Build(deps-dev): Bump tornado from 6.4 to 6.4.1 (#345)
- Build(deps): Bump urllib3 from 2.2.1 to 2.2.2 (#346)
- Build(deps-dev): Bump zipp from 3.18.0 to 3.19.1 (#347)
- Bumping Dependencies (#348)
- Build(deps-dev): Bump pytest-subtests from 0.13.0 to 0.13.1 (#349)
