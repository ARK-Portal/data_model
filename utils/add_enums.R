#! /usr/bin/Rscript

# add_enums.R
# $ Rscript add_enums.R -i input.json -m

suppressPackageStartupMessages({
  library(optparse)
  library(jsonlite)
  library(glue)
  library(dplyr)
})

# --------------------------------------------------------------------------- #
#  CLI arguments
# --------------------------------------------------------------------------- #
parser <- OptionParser() |>
  add_option(c("-i", "--inputJSON"),
             type = "character", default = NULL,
             help = "a json file defining enums to add per attribute"
  ) |>
  add_option(c("-m", "--modelCSV"),
             type = "character", default = NULL,
             help = "path to csv file to apply changes to."
  )

# read in and validate arguments
opt <- parse_args(parser)
test <- c("modelCSV", "inputJSON")
#for (opt_name in names(opt)) {
for (opt_name in test) {
  if (is.null(opt[[opt_name]])) {
    print_help(parser)
    stop(glue("Argument --{opt_name} is required. Exiting."), call. = FALSE)
  }
  if (!is.null(opt[[opt_name]]) && !file.exists(opt[[opt_name]])) {
    stop(glue("File not found: {opt[[opt_name]]}"), call. = FALSE)
  }
}

source("~/DCC/ARK Portal/coding/utils/data_model_tools.R")


new_enums <- read_json(opt$inputJSON, simplifyVector = FALSE)
df <- read.csv(opt$modelCSV)

df <- add_valid_val_bulk(additions = new_enums, model = df)

write_model_csv(df, opt$modelCSV)

message(glue("Enums added to {opt$modelCSV}!"))

# END