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
  templates.sort()
  return templates

def delete_templates(templates):
  for t in templates:
    print(f"Deleting template files for {t}...")
    csv_fid = f"model_templates/ark.{t}.csv"
    json_fid = f"model_templates/ark.{t}.schema.json"
    if os.path.exists(csv_fid):
      os.remove(csv_fid)
    if os.path.exists(json_fid):
      os.remove(json_fid)

####
#### concat context csv with all attr csv to make context model csv
####
for context in os.listdir("model_contexts/"):
  #print(context)
  path = f"model_contexts/{context}"
  contextCSV = pd.read_csv(f"{path}/ark.{context}_context.csv", dtype="object")
  context_attrs = list(contextCSV.Attribute)
  
  # read in and prep all attributes csv
  allAttr = pd.read_csv("ark.all_attributes.csv")
  allAttr = allAttr[allAttr.Attribute.isin(context_attrs) == False]
  
  # merge context and all attributes to create a model csv
  contextModel = pd.concat([contextCSV, allAttr], ignore_index=True)
  fid = f"{path}/ark.{context}_model.csv"
  contextModel.to_csv(fid, index=False, quoting=csv.QUOTE_ALL)
  
  # template management
  templates_fid = f"{path}/ark.{context}_templates.txt"
  templates = get_model_template_name(contextModel)
  # catalog changes to context templates
  if os.path.exists(templates_fid):
    with open(templates_fid, "r") as f:
      old_templates = [f.strip() for f in f.readlines()]
    f.close()
    del_templates = [t for t in old_templates if t not in templates]
    # delete template csv and json schema files
    delete_templates(del_templates)
  
  # write most up-to-date list of context templates to file
  with open(templates_fid, "w") as f:
    for t in set(templates):
      a = f.write(f"{t}\n")
  f.close()

print("\nAll context model csv files created!\n")



# END
