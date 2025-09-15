#! bin/bash

# generate_model_templates.sh.sh
# run schematic manifest get for all templates in each model context

# exit on error
set -e

CONTEXTS=( "model_contexts"/*/ )  # would match directories of depth 1

for context_dir in ${CONTEXTS[@]}; do
  context=$(basename "$context_dir")
  echo "Processing $context templates..."
  
  JSONLD="${context_dir}ark.${context}_model.jsonld"
  echo $JSONLD
  TEMPLATES="${context_dir}ark.${context}_templates.txt"
  while read template; do
    CSV="model_templates/ark.${template}.csv"
    OUTJSON="model_json_schema/ark.${template}.schema.json"
    ORIGJSON="${context_dir}ark.${context}_model.${template}.schema.json"
    #echo $CSV
    #echo $OUTJSON
    schematic manifest -c schematic_config.yml get -dt $template -o $CSV -p $JSONLD
    mv $ORIGJSON $OUTJSON
    
    # sleep for 10 seconds to keep google API from complaining
    sleep 10
  done < $TEMPLATES
done
