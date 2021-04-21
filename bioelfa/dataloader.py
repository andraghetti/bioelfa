#!/usr/local/bin/python3

"""
Dataloader for CSV into pandas dataframes
"""

import pandas
import pathlib

WORKSPACE_PATH = pathlib.Path(__file__).absolute().parent.parent

def load_csv(file_path: str) -> pandas.DataFrame:
    dataframe = pandas.read_csv(file_path, sep=';')
    return dataframe

def to_csv(dataframe: pandas.DataFrame, file_path: str):
    dataframe.to_csv(file_path, sep=';', index=False)
