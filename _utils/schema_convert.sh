#! bin/bash

# schema_convert.sh
# run schematic schema convert for every context-specific model

# exit on error
set -e

for context in model_contexts/*; do
  #echo $context
  for model in $context/*model.csv; do
    echo $model
    schematic schema convert $model
  done
done

echo -e "\nAll model csv have been converted to jsonld - done running schema convert.\n"