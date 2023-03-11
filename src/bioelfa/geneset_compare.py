import os
from pathlib import Path

import pandas as pd

from bioelfa import dataloader


def load_file(filepath: str):
    # Load CSV file
    csv_ext = os.extsep + 'csv'
    filepath = filepath if filepath.lower().endswith(csv_ext) else filepath + csv_ext
    dataframe = dataloader.load_csv(filepath, has_header=False)
    return dataframe


def split_and_unwrap_df(dataframe_column: pd.Series):

    dataframe_list = dataframe_column.fillna('').str.split('///').tolist()
    new_list = []

    # Iterate over the original list of lists
    for sublist in dataframe_list:
        # If the sublist has more than one element
        if sublist and len(sublist) > 1:
            new_list.extend(sublist)
        else:
            # Add the original entry to the new list
            new_list.append(sublist[0])
    return new_list


def count_occurences(dataframe) -> pd.DataFrame:
    # split entries in 'dataset1' into separate rows
    dataset1 = split_and_unwrap_df(dataframe.iloc[:, 0])
    dataset2 = split_and_unwrap_df(dataframe.iloc[:, 1])
    
    occurences = {
        elem: dataset1.count(elem)
        for elem in sorted(dataset2)
        if isinstance(elem, str) and elem != '0' and elem != ''
    }
    return pd.DataFrame(list(occurences.items()), columns=['Gene', 'Occurrences'])

def compare_datasets(filepath: str):
    """Loads a CSV file with two columns with genes in AGI format
    and counts the occurences of the second dataset in the first dataset.
    """
    dataframe = load_file(filepath)
    occurences = count_occurences(dataframe)
    outfile_path = Path("data/occurences.csv")
    dataloader.to_csv(occurences, str(outfile_path), index=True)
    print(f"Occurences file saved in: {outfile_path.absolute()}")
