# Data Models

## contexts_refactor branch

> This branch should not be merged with `gh-pages` or current `main` branch and vice versa

This repository contains the refactored ARK Portal data model. This version of the 
model uses "contexts" in order to have context-specific conditionally required 
attributes with the bonus of also being able to define context-specific valid value 
lists for model attributes and more. Ultimately we hope this produces an improved user 
experience when filling out metadata manifest templates generated from this data model.

The following subdirs are included in this branch:

`model_contexts/`: This directory houses each context-specific set of csv. Only the 
`model_context.csv` files should be modified to update contexts models. The other csv 
files are created through automated processes.

`model_json_schema/`: This directory stores all the json schema files generated from the 
various context-specific models. Note - all BDM-specific file annotation templates are 
deleted from this dir before committing changes to this branch b/c at this time the 
team does not have plans to bind these schema in Synapse (that may well change in the future).

3. `model_templates/`: This directory stores both XLSX- and CSV-formatted blank 
metadata templates. These files are created through automated processes. CSV templates 
are needed for creating template content on the data dictionary website (amongst other 
things).
