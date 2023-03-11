#!/usr/local/bin/python3

"""
Dataloader for CSV into pandas dataframes
"""

import pandas
import pathlib

WORKSPACE_PATH = pathlib.Path(__file__).absolute().parent.parent

def load_csv(file_path: str, has_header=True) -> pandas.DataFrame:
    dataframe = pandas.read_csv(file_path, sep=';', header=None if not has_header else 0)
    return dataframe

def to_csv(dataframe: pandas.DataFrame, file_path: str, index=False):
    dataframe.to_csv(file_path, sep=';', index=index)
