import os
import csv
import sys
import json

####
#### Functions
####
def json2csv(json_data, csv_fid):
    """
    Convert JSON data to CSV and save it to the specified file path.
    
    Parameters:
    json_data (list of dict): The JSON data to convert.
    csv_fid (str): The file path where the CSV will be saved.
    """
    columns = list(json_data['properties'].keys())
    out = ','.join(columns) + '\n'
    with open(csv_fid, 'w') as f:
        f.write(out)

def read_schema(fid):
  try:
    # Open the JSON file in read mode ('r')
    with open(fid, 'r') as file:
        # Load the JSON data from the file into a Python dictionary
        data = json.load(file)
    
    # Now you can work with the 'data' dictionary
    return(data)
  
  except FileNotFoundError:
      print(f"Error: The file '{fid}' was not found.")
  except json.JSONDecodeError:
      print(f"Error: Could not decode JSON from '{fid}'. Check if the file contains valid JSON.")
  except Exception as e:
      print(f"An unexpected error occurred: {e}")

####
#### MAIN
####
schema = os.listdir("model_json_schema/")
schema = [c for c in schema if c not in [".DS_Store", ".Rhistory"]] # for local execution

for s in schema:
    json_fid = os.path.join("model_json_schema", s)
    csv_fid = os.path.join("model_templates", s.replace(".schema.json", ".csv"))
    
    # Read JSON data from file
    json_data = read_schema(json_fid)
    
    # Convert JSON to CSV
    json2csv(json_data, csv_fid)
    
    print(f"Converted {json_fid} to {csv_fid}")




# END
