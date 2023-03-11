# Bioelfa

Set of utilities created for Ellen Fasth.

## Install

Install [conda](https://docs.conda.io/en/latest/miniconda.html) or create a virtual environment.
Activate the virtual environment and change directory to the root folder of the repository, then
install the package:

```sh
pip install .
```

## Commands

After installing, run the following command to see what's available:

```sh
bioelfa
```

# Example

For example, if you are in the root of the git repository, you can run:

```sh
bioelfa normalize data/bacteria_family.csv
```

and the result will be `data/normalized_bacteria_family.csv`. You can use absolute paths from anywhere in your computer. Note that the result will be a CSV file in the same path of the input file with a normalized_ prefix.

## Contributing

This package is open-source and everyone is welcomed to contribute and create PRs.

Some steps are necessary to get the right set-up to contribute:

- install all the dev dependencies `pip install -e .[dev]`
- install pre-commit hook: `pre-commit install`
- you can run the dashboard in develop mode if you want: `bioelfa dashboard -d`
- write your code, and create a pull-request on github on this repository.
