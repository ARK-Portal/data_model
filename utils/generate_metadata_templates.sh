#!/bin/bash
# generate blank xlsx templates

# exit on error
set -e

# create schematic config yml
echo "${SCHEMATIC_SERVICE_ACCOUNT_CREDS}" > schematic_service_account_creds.json
echo "✓ Created schematic_service_account_creds.json from secrets for template generation."

# generate list of templates defined in model
cut -f1 -d',' ark.model.csv | grep -i template > metadata_templates/templates.txt
sed -i 's/ //g' metadata_templates/templates.txt
sed -i 's/"//g' metadata_templates/templates.txt
sed -i 's/\([[:alpha:]]\)/\U\1/' metadata_templates/templates.txt
cat metadata_templates/templates.txt
echo "✓ Created metadata_templates/templates.txt."

# use schematic to generate xlsx for each template in templates.txt
while read template; do
  schematic manifest -c schematic_config.yml get -dt $template -oxlsx metadata_templates/$template.xlsx
  
  sleep 10 # prevent google API from complaining
  
done < metadata_templates/templates.txt
echo "✓ Created xlsx templates created."

# clean up/reorg remaining output from manifest get
mv *.schema.json metadata_templates/
echo "json schemas moved to metadata_templates/"

# clean up and remove sensitive info so it's not commited to repo
echo "Cleaning up directory"
rm -f schematic_service_account_creds.json

echo "✓ Done!"