#! Rscript

# install remote package
remotes::install_github("Sage-Bionetworks/JustTheDocsDataDictionary")
# load installed library
library(JustTheDocsDataDictionary)

args <- commandArgs(trailingOnly = TRUE)

# generate site content
main(args[1])

# END
