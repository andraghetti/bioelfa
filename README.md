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
normalize <your_csv_file_path>
```

### Example

For example, if you are in the root of the git repository, you can run:

```sh
normalize data/bacteria_family.csv
```

and the result will be `data/normalized_bacteria_family.csv`. You can use absolute paths from
anywhere in your computer. Note that the result will be a CSV file in the same path of the input
file with a `normalized_` prefix.

### Reproducibility

The seed is fixed to 0 to ensure reproducibility, and it can be changed adding the argument `--seed`
to the normalize command. For example:

```sh
normalize data/bacteria_family.csv --seed 90
```
