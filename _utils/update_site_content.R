#! Rscript

# install remote package
remotes::install_github("Sage-Bionetworks/JustTheDocsDataDictionary", ref = "dev")
# load installed library
library(JustTheDocsDataDictionary)

# generate site content
#main(args[1])
main(portal = "ark", template_list = "model_templates/templates.txt", branch = "main")

# END
