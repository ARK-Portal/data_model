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
    json_fid = f"model_json_schema/ark.{t}.schema.json"
    if os.path.exists(csv_fid):
      os.remove(csv_fid)
    if os.path.exists(json_fid):
      os.remove(json_fid)

def get_valid_values_dict(df):
  df = df[df['Valid Values'].isna() == False]
  df = df.loc[:, ["Attribute", "Valid Values"]]
  validvals = df.set_index("Attribute").to_dict("index")
  # split valid values into list
  for attribute in validvals.keys():
    validvals[attribute] = str(validvals[attribute]["Valid Values"])
    validvals[attribute] = validvals[attribute].replace(", ", ",")
    validvals[attribute] = validvals[attribute].replace(" ,", ",")
    validvals[attribute] = validvals[attribute].split(",")
  
  return validvals

def update_all_attributes(allAttr, vv):
  # update allAttr with valid values from all_vv
  for a in all_vv.keys():
    vv_string = ", ".join(all_vv[a])
    allAttr.loc[allAttr.Attribute == a, "Valid Values"] = vv_string
  # write updated all attributes csv
  allAttr.to_csv("ark.all_attributes.csv", index=False, quoting=csv.QUOTE_ALL)
  print("\nUpdated ark.all_attributes.csv with context-specific valid values!\n")
  
####
#### MAIN
####

# define list of contexts
contexts = os.listdir("model_contexts/")
contexts = [c for c in contexts if c not in [".DS_Store", ".Rhistory"]] # for local execution

# shore-up attribute valid values so that all context-specific valid values are included in all_attributes.csv
allAttr = pd.read_csv("ark.all_attributes.csv")
all_vv = get_valid_values_dict(allAttr)

# then compile context-specific valid values
for context in contexts:
  #print(context)
  path = f"model_contexts/{context}"
  contextCSV = pd.read_csv(f"{path}/ark.{context}_context.csv", dtype="object")
  # build dict of context-defined attributes with valid values
  context_vv = get_valid_values_dict(contextCSV)
  # update all_vv with any context-specific valid values
  for a in context_vv.keys():
    if a in all_vv.keys():
      # merge lists and remove duplicates
      merged = list(set(all_vv[a] + context_vv[a]))
      all_vv[a] = merged
    else:
      print(f"Error: {a} currently not defined in ark.all_attributes.csv with valid values. Please update.")
      sys.exit(1)

# adding any context-specific valid values to ark.all_attributes.csv just in case they weren't tracked there
update_all_attributes(allAttr, all_vv)

# read in newest version and prep all attributes csv
allAttr = pd.read_csv("ark.all_attributes.csv")
# create dictionary of attribute descriptions that can be pulled into context models
descriptions = allAttr.loc[:, ["Attribute", "Description"]].set_index("Attribute").to_dict("index")

# concat context csv with all attr csv to make context model csv
for context in contexts:
  #print(context)
  path = f"model_contexts/{context}"
  contextCSV = pd.read_csv(f"{path}/ark.{context}_context.csv", dtype="object")
  context_attrs = list(contextCSV.Attribute)
  common = [a for a in context_attrs if a in list(allAttr.Attribute)]
  # add a description to context csv if none exists
  for a in common:
    if contextCSV.loc[contextCSV.Attribute == a, "Description"].isna():
      contextCSV.loc[contextCSV.Attribute == a, "Description"] = descriptions[a]["Description"]
  
  # prep all attributes csv for merging
  temp_allAttr = allAttr[allAttr.Attribute.isin(context_attrs) == False]
  
  # merge context and all attributes to create a model csv
  contextModel = pd.concat([contextCSV, temp_allAttr], ignore_index=True)
  fid = f"{path}/ark.{context}_model.csv"
  contextModel.to_csv(fid, index=False, quoting=csv.QUOTE_ALL)
  
  # template management
  templates_fid = f"{path}/ark.{context}_templates.txt"
  templates = get_model_template_name(contextModel)
  # catalog changes to context templates
  if os.path.exists(templates_fid):
    old_templates = pd.read_table(templates_fid, header=None, names=["Template", "Context"])
    old_templates = list(old_templates.Template)
    del_templates = [t for t in old_templates if t not in templates]
    # delete template csv and json schema files
    delete_templates(del_templates)
  
  # write most up-to-date list of context templates to file
  with open(templates_fid, "w") as f:
    for t in set(templates):
      a = f.write(f"{t}\t{context}\n")
  f.close()

print("\nAll context model csv files created!\n")



# END
