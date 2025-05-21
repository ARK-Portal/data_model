# Data Models

## gh-pages branch

This branch contains all the files necessary for the ARK Portal data model dictionary 
site. 

> This branch should NOT be merged with `main` and vice versa

## Site Content

All site content is created using the `JustTheDocsDataDictionary` R package 
(<https://github.com/Sage-Bionetworks/JustTheDocsDataDictionary>). `_utils/update_site_content.R` 
installs and runs this package via the GitHub actions workflow `.github/workflows/ci-gh-pages.yml` 
which executes whenever there is a change to `ark.model.csv` in the main branch 
or changes to relevant files in the `gh-pages` branch. Site content changes are 
commited by this workflow which triggers site rebuild and deployment.

## Site Deployment

Github actions defined in `.github/workflows/pages.yml` is triggered when 
pushes are made affecting any site content files in this branch. See `.github/workflows/README.md` 
for more details.

### Local deployment and testing

Have `Ruby` and `RubyGems` installed on your system.

1. Install Jekyll `gem install bundler jekyll`
2. Install Bundler `bundle install`
3. (Option) Update Jekyll to resolve serve error `bundle update jekyll` (only needed if Gemfile.lock get out of date)
4. Run `bundle exec jekyll serve` to build your site and preview it at `http://localhost:4000`. The built site is stored in the directory `_site`.



