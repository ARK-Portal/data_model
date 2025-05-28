#!/bin/bash
# generate blank xlsx templates

# exit on error
set -e

# create schematic config yml
echo "${SCHEMATIC_SERVICE_ACCOUNT_CREDS}" > schematic_service_account_creds.json
echo "✓ Created schematic_service_account_creds.json from secrets for template generation."