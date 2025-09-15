import pandas as pd
import subprocess
import os
import csv
import sys
import time

####
#### Functions
####
def get_model_template_name(df):
  df = df[df.DependsOn.str.contains("Component") == True]
  templates = list(df.Attribute.unique())
  templates = [t.replace(" ", "") for t in templates]
  for i in range(len(templates)):
    nchar = len(templates[i])
    templates[i] = templates[i][0].capitalize() + templates[i][1:nchar]
  return templates

####
#### concat context csv with all attr csv to make context model csv
####
allAttr = pd.read_csv("ark.all_attributes.csv")
model_fids = []
templates = []

for context in os.listdir("model_contexts/"):
  #print(context)
  path = f"model_contexts/{context}"
  contextCSV = pd.read_csv(f"{path}/ark.{context}_context.csv")
  contextModel = pd.concat([contextCSV, allAttr], ignore_index=True)
  
  templates = get_model_template_name(contextModel)
  with open(f"{path}/ark.{context}_templates.txt", "w") as f:
    for t in set(templates):
      a = f.write(f"{t}\n")
  f.close()
  
  fid = f"{path}/ark.{context}_model.csv"
  model_fids.append(fid)
  contextModel.to_csv(fid, index=False, quoting=csv.QUOTE_ALL)

print("\nAll context model csv files created!\n")

# run schematic schema convert on each model csv
for context in os.listdir("model_contexts/"):
  path = f"model_contexts/{context}"
  model_csv = f"{path}/ark.{context}_model.csv"
  model_jsonld = f"{path}/ark.{context}_model.jsonld"
  #schematic schema convert ark.model.csv
  args = ["schematic", "schema", "convert", model_csv]
  result = subprocess.run(args, capture_output=True, text=True, check=True)
  print(result.stdout)
  if result.stderr:
    print(f"Error: {result.stderr}")
  
  # make csv templates for each context model
  with open(f"{path}/ark.{context}_templates.txt", "r") as f:
    templates = [t.rstrip('\n') for t in f.readlines()]
  for t in templates:
    out_csv = f"model_templates/ark.{t}.csv"
    out_json = f"model_json_schema/ark.{t}.schema.json"
    args = ["schematic", "manifest", "-c", "schematic_config.yml", "get", "-dt", t, "-p", model_jsonld, "-o", out_csv]
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    print(result.stdout)
    if result.stderr:
      print(f"Error: {result.stderr}")
    
    # manage json schema output
    orig = f"{path}/ark.{context}_model.{t}.schema.json"
    os.rename(orig, out_json)
    
    # sleep for 5 seconds to keep google API from complaining
    time.sleep(5)

print("\nDone!\n")



# END
