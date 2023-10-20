#!/bin/bash

# Used to build the documentation locally for testing/debug purposes.
# Nothing uses this script automatically!

python -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html
