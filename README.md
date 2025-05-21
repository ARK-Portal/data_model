# Data Models

## gh-pages branch

This branch contains all the files necessary for the ARK Portal data model dictionary 
site. 

> This branch should NOT be merged with `main` and vice versa

## Site Content

All site content is created by the Rscript in `_utils/update_site_content.R`. This 
script is executed via GitHub actions described in `main/.github/workflows/ci-gh-pages.yml` 
and will execute whenever there is a change to `ark.model.csv` in the main branch 
or changes to files under `_utils/` and `_templates` in the `gh-pages` branch. Any changes 
to site content are then automatically committed which will then trigger site re-deployment.

## Site Deployment

Github actions defined in `.github/workflows/pages.yml` is triggered when 
pushes are made affecting any file in the branch except those under `_utils/` and
`_templates`.

### Local deployment and testing

Have `Ruby` and `RubyGems` installed on your system.

1. Install Jekyll `gem install bundler jekyll`
2. Install Bundler `bundle install`
3. (Option) Update Jekyll to resolve serve error `bundle update jekyll` (only needed if Gemfile.lock get out of date)
4. Run `bundle exec jekyll serve` to build your site and preview it at `http://localhost:4000`. The built site is stored in the directory `_site`.



