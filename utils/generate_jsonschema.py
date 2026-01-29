from synapseclient import Synapse
from synapseclient.extensions.curator import generate_jsonschema
import pandas as pd

'''

'''

# create synapse client obj, this will be unnecessary in future client releases
syn = Synapse()

# read in compiled set of templates for each context
templates = pd.read_table("templates_by_context.txt", header=None)
templates.columns = ['template', 'context']
templates = templates.groupby(['context']).agg({'template': lambda x: list(x)}).reset_index()
templates = templates.set_index('context').to_dict()['template']

for context in templates.keys():
    print(f"Generating JSON schemas for context: {context}")
    for t in templates[context]:
      try:
        schemas, file_paths = generate_jsonschema(
          data_model_source=f"model_contexts/{context}/ark.{context}_model.csv",
          output=f"model_json_schema/ark.{t}.schema.json",
          data_types= [t],
          synapse_client=syn
        )
        print("Success!")
      except Exception as e:
        print(f"Error generating schema for template '{t}' in context '{context}': {e}")


schemas, file_paths = generate_jsonschema(data_model_source= "model_contexts/clinical/ark.clinical_model.csv",
                                          output= "model_json_schema/ark.test.schema.json",
                                          data_types= ['ClinicalMetadataTemplate'],
                                          synapse_client= syn
                                          )
test = pd.read_csv("model_contexts/clinical/ark.clinical_model.csv")
                                          
