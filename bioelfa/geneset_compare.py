import os
import dataloader
import argparse
import pandas as pd
from pathlib import Path


def load_file():
    parser = argparse.ArgumentParser(description=count_occurences.__doc__)
    parser.add_argument('filepath', metavar='CSV_FILE', type=str,
                        help='path to a csv file with two columns of genes in AGI format to compare')

    args = parser.parse_args()

    # Load CSV file
    csv_ext = os.extsep + 'csv'
    filepath = args.filepath if args.filepath.lower().endswith(csv_ext) else args.filepath + csv_ext
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

def main():
    dataframe = load_file()
    occurences = count_occurences(dataframe)
    filepath = Path("data/occurences.csv")
    dataloader.to_csv(occurences, filepath, index=True)
    print(f"Occurences file saved in: {filepath.absolute()}")

if __name__ == "__main__":
    main()
