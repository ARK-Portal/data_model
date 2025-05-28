#!/bin/bash
# test to see how json is getting written from secrets

# exit on error
set -e

# define script variables
CREDS=./schematic_service_account_creds.json

# create schematic config yml
echo "${SCHEMATIC_SERVICE_ACCOUNT_CREDS}" > $CREDS
echo "✓ Created temp $CREDS from secrets for template generation."

cat schematic_service_account_creds.json