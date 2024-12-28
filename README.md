# Data Models

## main branch

> This branch should not be merged with `gh-pages` and vice versa

This repository contains 3 major files:

1. `ark.model.csv`: The CSV representation of the ARK Portal data model and is used 
to create the JSON-LD representation of the data model.


2. `ark.model.jsonld`: The JSON-LD representation of the data model, which is 
automatically created from the CSV data model using the schematic CLI. More details 
on how to convert the CSV data model to the JSON-LD data model can be 
found [here](https://sage-schematic.readthedocs.io/en/develop/cli_reference.html#schematic-schema-convert). 
This is the central schema (data model) which will be used to power the 
generation of metadata manifest templates for various data types (e.g., `scRNA-seq Level 1`) 
from the schema.


3. `schematic_config.yml`: A template version of the schematic-compatible configuration file, 
which allows users to specify values for application-specific keys (e.g., path 
to Synapse configuration file) and project-specific keys (e.g., Synapse 
fileview for community project). A description of what the various keys in this 
file represent can be found in the [Fill in Configuration File(s)](https://sage-schematic.readthedocs.io/en/develop/README.html#fill-in-configuration-file-s) 
section of the schematic [docs](https://sage-schematic.readthedocs.io/en/develop/index.html).
