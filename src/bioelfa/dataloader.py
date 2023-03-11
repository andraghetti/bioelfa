#!/usr/local/bin/python3

"""
Dataloader for CSV into pandas dataframes
"""

import pandas
import pathlib
import os

from typing import Tuple, Union, Any

WORKSPACE_PATH = pathlib.Path(__file__).absolute().parent.parent

def load_csv(file: Union[str, Any], has_header=True) -> pandas.DataFrame:
    csv_ext = os.extsep + 'csv'
    if isinstance(file, str):  # path
        file = file if file.lower().endswith(csv_ext) else file + csv_ext
    dataframe = pandas.read_csv(file, sep=';', header=None if not has_header else 0)
    return dataframe

def to_csv(dataframe: pandas.DataFrame, file_path: str, index=False):
    dataframe.to_csv(file_path, sep=';', index=index)
