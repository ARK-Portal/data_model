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

### Catalog existing md files, those attributes no longer in the model will be archived
get_md_cat <- function(){
  md_dirs <- c("_includes/content/", 
             "docs/metadata_templates/", 
             "docs/attributes/")
  md_catalog <- purrr::map(md_dirs, function(dir) {
    out <- data.frame(full_name = list.files(dir, full.names = TRUE))
    return(out)
  })
  md_catalog <- bind_rows(md_catalog)
  md_catalog$Attribute <- unlist(purrr::map(md_catalog$full_name,
                                            function(fid) {
                                              basename(fid) %>% str_remove(pattern = "\\.md")
                                            }))
  return(md_catalog)
}

get_title_snake <- function(x) {
  title_snake <- snakecase::to_snake_case(x)
  title_snake <- str_replace(title_snake, "sc_rna_seq", "scrnaseq")
  return(title_snake)
}

archive_md <- function(fid) {
  file.rename(from = fid, to = glue(".archived/{fid}"))
}

content_md <- function(attr, desc, vals_note = FALSE) {
  fid <- glue("_includes/content/{attr}.md")
  if (!file.exists(fid)) {
    if (desc == ""){
      md_lines <- "Content TBD"
    } else{
      md_lines <- c(desc)
    }
    if (vals_note){
      md_lines <- c(md_lines, "\n", 
                    "{: .note }",
                    "There are no defined valid values for this model attribute.")
    }
    writeLines(md_lines, con = fid)
  }
}

#################
###   SETUP   ###
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
fid <- "https://raw.githubusercontent.com/ARK-Portal/data_models/refs/heads/main/ark.model.csv"
model <- read.csv(fid)

# split into constituent parts
model_templates <- filter(model, grepl("template", Attribute, ignore.case = TRUE) |
                            grepl("^Component", DependsOn))

valid_vals <- get_validVals(model)
model_attributes <- filter(model, 
                           Attribute %notin% c(model_templates$Attribute, valid_vals))
# order alphabetically and add nav_order rank
model_attributes$rank <- str_to_lower(model_attributes$Attribute)
model_attributes <- arrange(model_attributes, rank)
model_attributes$rank <- 1:nrow(model_attributes)
# df with attributes with valid values
model_valid_val <- filter(model_attributes, Valid.Values != "")

###############
### Archive ###
###############
## archive content for attributes no longer in the model
## get catalog of existing md files
md_catalog <- get_md_cat()
# ignore parent md files
md_catalog <- filter(md_catalog, Attribute %notin% c("attributes", "metadata_templates"))
# select those no longer in model
template_str <- unlist(purrr::map(model_templates$Attribute, get_title_snake))
md_catalog <- filter(md_catalog, Attribute %notin% c(model$Attribute, template_str))
# archive files that remain in md_catalog
if (nrow(md_catalog) > 0) {
  purrr::walk(c(".archived/", ".archived/_includes/", 
                ".archived/_includes/content/", 
                ".archived/docs/",
                ".archived/docs/metadata_templates/", 
                ".archived/docs/attributes/"), 
              make_subdir)
  purrr::walk(md_catalog$full_name, archive_md)
}

###############
####  CSV  ####
###############
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
               title_snake <- get_title_snake(attr)
               depends <- unlist(strsplit(depends, ", "))
               out <- filter(df, Attribute %in% depends)
               out$Attribute <- factor(out$Attribute, levels = depends)
               out <- select(out, Attribute, Description, Required, Valid.Values)
               out <- arrange(out, Attribute)
               #print(head(out))
               fid = glue("_data/csv/metadata_templates/{title_snake}.csv")
               write_model_csv(out, fid)
             }, df = model)

###############
## MD files  ##
###############
### metadata templates Markdown files
### docs/metadata_templates/ one md per template
purrr::pwalk(select(model_templates, Attribute, DependsOn, Description),
             function(Attribute, DependsOn, Description){
               title_snake <- get_title_snake(Attribute)
               
               # make content md file is doesn't exist
               content_md(title_snake, Description, vals_note = FALSE)
               
               depends <- str_replace_all(DependsOn, ", ", "', '")
               depends <- glue("'{depends}'")
               output <- glue("docs/metadata_templates/{title_snake}.md")
               #cmd <- glue("Rscript _utils/render_template.R metadata_template {output} '{Attribute}' {title_snake} \"{depends}\"")
               run <- sys::exec_internal(cmd = "Rscript", 
                                         args = c("_utils/render_template.R", 
                                         "metadata_template", 
                                         output, glue('{Attribute}'),
                                         "title_snake", glue("\"{depends}\"")))
               if (run$status != 0) {
                stop(glue("Failed to complete execution of _utils/render_template.R for {title_snake}"))
               }
             })

### attributes with valid values
purrr::pwalk(select(model_valid_val, Attribute, Description, rank),
            function(Attribute, Description, rank){
              # make content md file is doesn't exist
              content_md(Attribute, Description, vals_note = FALSE)
              
              output <- glue("docs/attributes/{Attribute}.md")
              run <- sys::exec_internal(cmd = "Rscript", 
                                        args = c("_utils/render_template.R", 
                                                 "valid_vals",  
                                                 output, Attribute, rank))
              if (run$status != 0) {
                stop(glue("Failed to complete execution of _utils/render_template.R for {Attribute}"))
              }
            })


### attributes w/o valid values
purrr::pwalk(filter(model_attributes, Valid.Values == "") %>% 
                      select(Attribute, Description, rank), 
             function(Attribute, Description, rank){
               # make content md file is doesn't exist
               content_md(Attribute, Description, vals_note = TRUE)
               
               output <- glue("docs/attributes/{Attribute}.md")
               run <- sys::exec_internal(cmd = "Rscript", 
                                         args = c("_utils/render_template.R", 
                                                  "attribute",  
                                                  output, Attribute, rank))
               if (run$status != 0) {
                 stop(glue("Failed to complete execution of _utils/render_template.R for {Attribute}"))
               }
             })

writeLines("Success!")

# END