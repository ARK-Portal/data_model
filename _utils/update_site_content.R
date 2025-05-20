#! Rscript

library(JustTheDocDataDictionary)

args <- commandArgs(trailingOnly = TRUE)

#data_model_url <- "https://raw.githubusercontent.com/ARK-Portal/data_model/refs/heads/main/ark.model.csv"
main(args[1])

# END
