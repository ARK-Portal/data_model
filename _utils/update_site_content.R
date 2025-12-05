#! Rscript

# install remote package
remotes::install_github("Sage-Bionetworks/JustTheDocsDataDictionary", ref = "dev")
# load installed library
library(JustTheDocsDataDictionary)

# generate site content
#main(args[1])
#main(portal = "ark", branch = "main")

# generate site content from context-based model design
main_contexts(portal = "ark",
              template_dir = "model_templates",
              branch = "main")

# END
