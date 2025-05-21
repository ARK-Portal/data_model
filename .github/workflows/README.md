# Repo GitHub Actions Workflows

`ci-schema-convert.yml`
- triggered on PR to `main` w/mods to model.csv or this yml file
- runs `schematic schema convert` to generate model.jsonld from model.csv
  - commits change to PR branch

`ci-gh-pages.yml`
- triggered on
  - push to `main` that changes model.csv
  - push to `gh-pages` that scripts or templates used to generate site content
  - push to `main` or `gh-pages` that changes this yml file

`pages.yml`
- triggered on pushed to `gh-pages` that change site content or this yml file
- builds and deploys Jekyll site