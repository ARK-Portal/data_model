import pandas as pd
import subprocess
import os
import csv
import sys
import time

'''
this script will take each context.csv and combine with the ark.all_attributes.csv 
to generate context-specific model csv files.
'''

####
#### Functions
####
def get_model_template_name(df):
  #df = df[df.Attribute.str.contains("Template|Annotation") == True]
  df['IsTemplate'] = df['IsTemplate'].map({'TRUE': True, 'FALSE': False})
  df = df[df['IsTemplate']]
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
    fid_ext = {"csv": "model_templates", "schema.json": 'model_json_schema', "xlsx": "model_templates"}
    for e in fid_ext.keys():
      fid = f"{fid_ext[e]}/ark.{t}.{e}"
      if os.path.exists(fid):
        os.remove(fid)
        print(f"{fid} deleted.")

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

def manage_columnType_conversion_descriptions(df):
  # if attribute is no longer a list-type in the context model
  # modify the attribute description accordingly
  to_remove = [" Multiple selections can be provided in a comma-delimited list.", 
               " For multi-specimen data files provide all IDs in a comma-separated list."]
  non_list_df = df[df.columnType.str.contains("_list", na=False) == False]
  non_list_df.reset_index(drop = True, inplace = True)
  desc = []
  for d in non_list_df.Description:
    for x in to_remove:
      d = d.replace(x, "")
    desc.append(d)
  
  idx = non_list_df.columns.get_loc('Description')
  non_list_df.iloc[:, idx] = desc
  
  df = df[df['columnType'].str.contains("_list", na=False) == True]
  out = pd.concat([df, non_list_df], ignore_index=True)
  return out


def update_all_attributes(allAttr, vv):
  # update allAttr with valid values from all_vv
  for a in all_vv.keys():
    # sort alphabetically
    all_vv[a].sort()
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
allAttr = pd.read_csv("ark.all_attributes.csv", dtype="object")
all_vv = get_valid_values_dict(allAttr)

# then compile context-specific valid values
new_rows = [] # a list to hold any new attributes to be added to allAttr later
add_new_rows = False # logical variable to indicate if new rows need to be added to allAttr
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
      print(f"Warning: '{a}' is currently not defined as an attribute in ark.all_attributes.csv *with valid values*.")
      #sys.exit(1)
      if a not in list(allAttr.Attribute):
        add_new_rows = True # logical variable to indicate if new rows need to be added to allAttr
        print(f"'{a}' does not exist in ark.all_attributes.csv and will be added as is defined in {context}.")
        # collect new attr in dict to be added to allAttr at a later time
        #new_row = contextCSV[contextCSV.Attribute == a].iloc[0]
        new_row = contextCSV.loc[contextCSV.Attribute == a, :]
        new_rows.append(new_row)
      else:
        # add context-specific valid values to all_vv
        print(f"'{a}' context-specific valid values will be added to the attribute in ark.all_attributes.csv.")
        all_vv[a] = context_vv[a]

if add_new_rows:
  df = pd.concat(new_rows)
  #df.to_csv("temp_new_attributes.csv", index=False, quoting=csv.QUOTE_ALL) # testing purposes
  allAttr = pd.concat([allAttr, df], ignore_index=True)
  # sanity check for duplicated attributes
  if allAttr.Attribute.duplicated().any():
    print("Error: Duplicated attributes found in ark.all_attributes.csv after adding new attributes from contexts.")
    sys.exit(1)

# adding any context-specific valid values to ark.all_attributes.csv just in case they weren't tracked there
update_all_attributes(allAttr, all_vv)

# read in newest version and prep all attributes csv
allAttr = pd.read_csv("ark.all_attributes.csv", dtype="object")
# create dictionary of attribute descriptions that can be pulled into context models
descriptions = allAttr.loc[:, ["Attribute", "Description"]].set_index("Attribute").to_dict("index")

# concat context csv with all attr csv to make context model csv
master_template_df = {"template": [], 'context': []}
for context in contexts:
  #print(context)
  path = f"model_contexts/{context}"
  contextCSV = pd.read_csv(f"{path}/ark.{context}_context.csv", dtype="object")
  context_attrs = list(contextCSV.Attribute)
  common = [a for a in context_attrs if a in list(allAttr.Attribute)]
  # add a description to context csv if none exists
  for a in common:
    if contextCSV.loc[contextCSV.Attribute == a, "Description"].isna().any():
      contextCSV.loc[contextCSV.Attribute == a, "Description"] = descriptions[a]["Description"]
  
  # if attribute has defined enums/valid vals in all_attributes but not in context csv
  # then add all enums in context, this makes it easy to have context-specific column types
  df = contextCSV[contextCSV.Attribute.isin(list(all_vv.keys())) == True] # get context Attributes that have enums in all_attr
  df.reset_index(drop = True, inplace = True)
  
  df = df[df['Valid Values'].isna()] # now have context Attr that don't have context-specific enums list
  df.reset_index(drop = True, inplace = True)
  # add all_attr vv to context attr
  for x in range(0, df.shape[0]):
    a = df.Attribute.to_list()[x]
    vv = ', '.join(all_vv[a])
    df.loc[x, 'Valid Values'] = vv
  # then bring it all together
  contextCSV = contextCSV[contextCSV.Attribute.isin(df.Attribute.to_list()) == False]
  contextCSV = pd.concat([contextCSV, df], ignore_index=True)
  contextCSV.reset_index(drop = True, inplace = True)
  
  # prep all attributes csv for merging by removing any context specific attr entries
  temp_allAttr = allAttr[allAttr.Attribute.isin(context_attrs) == False]
  
  # merge context and all attributes to create a model csv
  contextModel = pd.concat([contextCSV, temp_allAttr], ignore_index=True)
  contextModel = manage_columnType_conversion_descriptions(contextModel)
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
    sorted_uniq_list = sorted(list(set(templates)))
    #for t in set(templates):
    for t in sorted_uniq_list:
      a = f.write(f"{t}\t{context}\n")
      # add to 'master' dictionary for writing templates_by_context.txt
      master_template_df['template'].append(t)
      master_template_df['context'].append(context)
  f.close()


df = pd.DataFrame(master_template_df)
df.sort_values(by=['context', 'template'], inplace=True)
df.to_csv('templates_by_context.txt', sep='\t', header=False, index=False)


print("\nAll context model csv files created!\n")



# END
