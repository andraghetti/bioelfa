#!/usr/local/bin/python3

"""
Dataloader for CSV into pandas dataframes
"""

import pandas
import pathlib

WORKSPACE_PATH = pathlib.Path(__file__).absolute().parent.parent
DATA_PATH = WORKSPACE_PATH / 'data'

def load_csv(filename: str) -> pandas.DataFrame:
    file_path = DATA_PATH / filename
    dataframe = pandas.read_csv(file_path, sep=';')
    return dataframe

def to_csv(dataframe: pandas.DataFrame, filename: str):
    dataframe.to_csv(DATA_PATH / filename, sep=';', index=False)
