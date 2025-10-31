#!/bin/bash
# generate blank xlsx templates

# exit on error
set -e

# create schematic config yml
echo "${SCHEMATIC_SERVICE_ACCOUNT_CREDS}" > schematic_service_account_creds.json
echo "✓ Created schematic_service_account_creds.json from secrets for template generation."

# generate list of templates defined in model
cut -f1 -d',' ark.model.csv | grep -i template > model_templates/templates.txt
sed -i 's/ //g' model_templates/templates.txt
sed -i 's/"//g' model_templates/templates.txt
sed -i 's/\([[:alpha:]]\)/\U\1/' model_templates/templates.txt
cat model_templates/templates.txt
echo "✓ Created model_templates/templates.txt."

# use schematic to generate xlsx for each template in templates.txt
while read template; do
  schematic manifest -c schematic_config.yml get -dt $template -oxlsx model_templates/$template.xlsx
  
  sleep 10 # prevent google API from complaining
  
done < model_templates/templates.txt
echo "✓ Created xlsx templates created."

# clean up/reorg remaining output from manifest get
mv *.schema.json model_templates/
echo "json schemas moved to model_templates/"

echo "✓ Done!"

# END