#! bin/bash

# generate_model_templates.sh.sh
# run schematic manifest get for all templates in each model context

# exit on error
set -e

ALL_TEMPLATES=()
CONTEXTS=( "model_contexts"/*/ )  # would match directories of depth 1

for context_dir in ${CONTEXTS[@]}; do
  context=$(basename "$context_dir")
  echo "Processing $context templates..."
  
  JSONLD="${context_dir}ark.${context}_model.jsonld"
  echo $JSONLD
  TEMPLATES="${context_dir}ark.${context}_templates.txt"
  ALL_TEMPLATES+=("$TEMPLATES") # Append a new element in each iteration
  while read template; do
    # generate xlsx templates
    #CSV="model_templates/ark.${template}.csv"
    XLSX="model_templates/ark.${template}.xlsx"
    OUTJSON="model_json_schema/ark.${template}.schema.json"
    ORIGJSON="${context_dir}ark.${context}_model.${template}.schema.json"
    #echo $CSV
    #echo $OUTJSON
    schematic manifest -c schematic_config.yml get -dt $template -oxlsx $XLSX -p $JSONLD
    #mv $ORIGJSON $OUTJSON
    
    if [ -f model_templates/ark.xlsx ]; then
      mv model_templates/ark.xlsx $XLSX # schematic 24.11.2 bug only writes output to this when executed locally for some weird reason
    fi
    
    # generate json schema
    rm $ORIGJSON # delete json schema created using old schematic functions
    # make json schema using new schematic functions
    #ORIGJSON2="temp/ark.${context}_model/${template}_validation_schema.json"
    schematic schema generate-jsonschema -dms $JSONLD -dt $template -od temp -dml class_label
    mv $ORIGJSON $OUTJSON
    #mv $ORIGJSON2 $OUTJSON
    
    # sleep for 10 seconds to keep google API from complaining
    sleep 10
  done < <(cut -f 1 $TEMPLATES)
done

# clean up superfluous temp files
rm -Rf temp/

# concat all template files into one
if [ -f templates_by_context.txt ]; then
  rm templates_by_context.txt
fi
for template in ${ALL_TEMPLATES[@]}; do
  cat $template >> templates_by_context.txt
done

# delete BDM-specific json schema files
rm model_json_schema/ark.BDM*
