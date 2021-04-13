# Bioelfa

Set of utilities created for Ellen Fasth.

## Install
Install [conda](https://docs.conda.io/en/latest/miniconda.html) or create a virtual environment.
Activate the virtual environment and change directory to the root folder of the repository, then
install the package:

```sh
pip install -e bioelfa/
```

## Command: `normalize`
This command normalizes the reads by a threshold T (the smallest number of total reads among all the
samples) of a CSV file containing gene reads.

Once the virtual environment is activated and the package is installed, you can simply run:

```sh
normalize
```

NOTE: it will take as default the file `data/bacteria_family.csv`. A file path as input will come
in the next version.

The result will be `data/normalized_bacteria_family.csv`.
