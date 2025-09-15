import pandas as pd
import subprocess
import os
import csv
import sys

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
  
  templates = templates + get_model_template_name(contextCSV)
  
  fid = f"{path}/ark.{context}_model.csv"
  model_fids.append(fid)
  contextModel.to_csv(fid, index=False, quoting=csv.QUOTE_ALL)

# prepare for template generation
with  open("model_templates/templates.txt", "w") as f:
  for t in set(templates):
    a = f.write(f"{t}\n")
f.close()

# run schematic schema convert on each model csv
for fid in model_fids:
#schematic schema convert ark.model.csv
result = subprocess.run(["schematic", "schema", "convert", fid], capture_output=True, text=True, check=True)
print(result.stdout)
if result.stderr:
  print(f"Error: {result.stderr}")


print("\nDone!\n")

# END
