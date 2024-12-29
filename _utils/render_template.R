#! /usr/local/bin/R
# _utils/render_template.R

args <- commandArgs(trailingOnly = TRUE)
# 1 = rmd template to use
# 2 = output file
# 3 = title
# 4 = title_snake or rank
# 5 = dependsOn

if (args[1] == "metadata_template"){
  suppressMessages(
    rmarkdown::render(
      input = "_templates/template-metadata_templates.Rmd",
      run_pandoc = FALSE,
      runtime = 'static',
      knit_root_dir = "../",
      #output_file = args[2],
      output_format = 'md_document', 
      params = list("title" = args[3], 
                    "title_snake" = args[4], 
                    "dependsOn" = args[5])
    )
  )

  temp <- file.rename(from = "_templates/template-metadata_templates.knit.md", 
                      to = args[2])
}

if (args[1] == "valid_vals"){
  rmarkdown::render(
    input = "_templates/template-valid_vals.Rmd",
    run_pandoc = FALSE,
    runtime = 'static',
    knit_root_dir = "../",
    #output_file = args[2],
    output_format = 'md_document', 
    params = list("title" = args[3], "rank" = args[4])
  )

  temp <- file.rename(from = "_templates/template-valid_vals.knit.md", 
                      to = args[2])
}

if (args[1] == "attribute"){
  rmarkdown::render(
    input = "_templates/template-attributes.Rmd",
    run_pandoc = FALSE,
    runtime = 'static',
    knit_root_dir = "../",
    #output_file = args[2],
    output_format = 'md_document', 
    params = list("title" = args[3], "rank" = args[4])
  )
  
  temp <- file.rename(from = "_templates/template-attributes.knit.md", 
                      to = args[2])
}

if (temp) {
  writeLines(paste(args[2], "written."))
}



