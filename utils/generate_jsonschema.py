from synapseclient import Synapse
from synapseclient.extensions.curator import generate_jsonschema
import pandas as pd

'''
use synapseclient extension to create Curator json schema from context models
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
    schemas, file_paths = generate_jsonschema(
      data_model_source=f"model_contexts/{context}/ark.{context}_model.csv",
      output=f"model_json_schema/ark.{t}.schema.json",
      data_types= [t],
      synapse_client=syn,
      data_model_labels = "display_label"
    )

print("JSON schema generation complete!")

# END
