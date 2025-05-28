#!/bin/bash
# test to see what gets written using fake json

# exit on error
set -e
CREDS=./fake.json

# create schematic config yml
echo "${FAKE_JSON}" > $CREDS
echo "✓ Created temp $CREDS from secrets for template generation."