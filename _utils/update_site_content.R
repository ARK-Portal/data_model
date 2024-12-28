#! Rscript

# update_site_content.R

#################
### Functions ###
#################
`%notin%` <- Negate(`%in%`)

make_subdir <- function(d) {
  if (!dir.exists(d)) {
    dir.create(d)
  }
}

get_validVals <- function(df){
  temp <- filter(df, !grepl("^$", Valid.Values) & !is.na(Valid.Values))
  valid_vals <- purrr::map(temp$Valid.Values, function(d){
    unlist(strsplit(d, ", "))
  })
  valid_vals <- unique(unlist(valid_vals))
}

# write schematic data model in correct csv format
write_model_csv <- function(df, fid) {
  df[is.na(df)] <- ""
  colnames(df) <- stringr::str_replace_all(colnames(df), "\\.", " ")
  write.csv(df, file = fid, quote = TRUE, row.names = FALSE, na = "")
}

#################
###   Setup   ###
#################

# Load libraries silently
suppressPackageStartupMessages({
  library(dplyr)
  library(stringr)
  library(glue)
  library(readr)
  library(yaml)
  
})

# download latest version of data model
model <- read.csv("https://raw.githubusercontent.com/ARK-Portal/data_models/refs/heads/main/ark.model.csv")
# split into consituent parts
model_templates <- filter(model, grepl("template", Attribute, ignore.case = TRUE) |
                            grepl("^Component", DependsOn))

valid_vals <- get_validVals(model)
model_attributes <- filter(model, 
                           Attribute %notin% c(model_templates$Attribute, valid_vals))
model_valid_val <- filter(model_attributes, Valid.Values != "")

#### Valid Value CSV _data/csv/attributes/
purrr::walk2(model_valid_val$Attribute, model_valid_val$Valid.Values, 
             function(attr, vals) {
                vals <- unlist(str_split(vals, ", ")) %>% sort()
                out <- tibble('Valid Values' = as.character(vals))
                # check for existing definitions
                fid <- glue("_data/csv/attributes/{attr}.csv")
                if (file.exists(fid)) {
                  pre <- read.csv(fid, colClasses = rep("character", 3)) %>% tibble()
                  colnames(pre) <- c("Valid Values", "Description", "Source")
                  # merge into valid values in model
                  out <- left_join(out, pre, by = "Valid Values")
                } else {
                  out$Description <- NA
                  out$Source <- NA
                }
                out <- arrange(out, `Valid Values`) %>% unique()
                write_csv(out, 
                          file = glue("_data/csv/attributes/{attr}.csv"), 
                          quote = "all", na = "")
              })

#### Metadata Template CSV _data/csv/metadata_templates/
purrr::walk2(model_templates$Attribute, model_templates$DependsOn,
             function(attr, depends, df) {
               title_snake <- snakecase::to_snake_case(attr)
               title_snake <- str_replace(title_snake, "sc_rna_seq", "scrnaseq")
               depends <- unlist(strsplit(depends, ", "))
               out <- filter(df, Attribute %in% depends)
               out$Attribute <- factor(out$Attribute, levels = depends)
               out <- select(out, Attribute, Description, Required, Valid.Values)
               out <- arrange(out, Attribute)
               #print(head(out))
               fid = glue("_data/csv/metadata_templates/{title_snake}.csv")
               write_model_csv(out, fid)
             }, df = model)

### Catalog existing
md_dirs <- c("_includes/content/", 
             "docs/metadata_templates/", 
             "docs/attributes/")
md_catalog <- purrr::map(md_dirs, function(dir) {
                           md <- list.files(dir, full.names = TRUE)
                           return(md)
                         })

### metadata templates Markdown files
### docs/metadata_templates/ one md per template
purrr::walk2(model_templates$Attribute, model_templates$DependsOn,
             function(attr, depends){
               title_snake <- snakecase::to_snake_case(attr)
               title_snake <- str_replace(title_snake, "sc_rna_seq", "scrnaseq")
               depends <- str_replace_all(depends, ", ", "', '")
               depends <- glue("'{depends}'")
               output <- glue("docs/metadata_templates/{title_snake}.md")
               cmd <- glue("Rscript _utils/render_template.R metadata_template {output} '{attr}' {title_snake} \"{depends}\"")
               run <- sys::exec_internal(cmd = "Rscript", 
                                         args = c("_utils/render_template.R", 
                                         "metadata_template", 
                                         output, glue('{attr}'),
                                         "title_snake", glue("\"{depends}\"")))
               if (run$status != 0) {
                stop("Failed to complete execution of _utils/render_template.R")
               }
             })

writeLines("Success!")

# END