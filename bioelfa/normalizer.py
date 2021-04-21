#!/usr/local/bin/python3

"""
This module has the utilities to normalize the reads by a threshold T (the smallest number of total
reads among all the samples). To normalize, we get the threshold and then we randomly pick T reads
from each sample.
NOTE:
- column -> sample
- row -> family
- cell -> number of reads of a certain family in a sample
"""

import argparse
import os

import numpy
import pandas
from tqdm import tqdm

import dataloader


def get_reads_threshold(dataframe: pandas.DataFrame) -> (int, str):
    """
    This function gets the reads-threshold from the dataframe, which means taking the minimum number
    of the total reads per sample (columns).
    It returns a tuple with the threshold (int) and the sample name (str)
    """

    # Calculate the total reads for each sample
    total_reads = {}
    for sample in dataframe.columns[1:]:
        total_reads[sample] = dataframe[sample].sum()

    # Select the minimum number of total reads
    threshold = min([val for val in total_reads.values()])
    for sample, total in total_reads.items():
        if total == threshold:
            break

    return threshold, sample


def get_occurrences(non_zero_rows_values, non_zero_indexes, threshold):
    """Dictionary with:
    key: row index
    value: occurrences
    """
    # print(non_zero_indexes)
    # print(non_zero_rows_values)
    index_list = numpy.array(non_zero_indexes)
    index_list = numpy.repeat(non_zero_indexes, non_zero_rows_values)
    numpy.random.shuffle(index_list)
    sampled_index_list = index_list[:threshold]

    occurrences = {}
    total_reads = 0
    for index in non_zero_indexes:
        occurrence = numpy.count_nonzero(sampled_index_list==index)
        occurrences[index] = occurrence
        total_reads += occurrence
    # print(f'total_reads: {total_reads}')
    return occurrences



def normalize_data(dataframe: pandas.DataFrame, threshold: int) -> pandas.DataFrame:
    """
    To normalize, we get the threshold T and then we randomly pick T reads from each sample.
    """
    # Initialize the selected dataframe to zeros
    selected = pandas.DataFrame().reindex_like(dataframe).fillna(0).astype(int)
    selected['ID'] = dataframe['ID']

    # For each sample, select T reads if not empty
    for sample_name in tqdm(dataframe.columns[1:], unit=' samples'):
        # Get occurrences of each family 
        sample_column = dataframe[sample_name]
        non_zero_families_reads = sample_column.loc[sample_column != 0].tolist()
        non_zero_families_indexes = dataframe.index[sample_column != 0].tolist()
        occurrences = get_occurrences(non_zero_families_reads, non_zero_families_indexes, threshold)

        # Replace the zeros with the sampled reads
        for family_index, num_reads in occurrences.items():
            selected.loc[family_index, sample_name] = num_reads
    return selected

def normalize():
    """
    Entrypoint fuctionto normalize the reads by a threshold T (the smallest number of total
    reads among all the samples). To normalize, we get the threshold and then we randomly pick T reads
    from each sample.
    """
    parser = argparse.ArgumentParser(description=normalize.__doc__)
    parser.add_argument('filepath', metavar='CSV_FILE', type=str,
                        help='path to a csv file representing a gene reads table to normalize')
    parser.add_argument('--seed', type=int, default=0,
                        help='the seed used to initialize the random generator for the sampling '
                             'operation. Defaults to 0')

    args = parser.parse_args()

    # Load CSV file
    csv_ext = os.extsep + 'csv'
    filepath = args.filepath if args.filepath.lower().endswith(csv_ext) else args.filepath + csv_ext
    dataframe = dataloader.load_csv(filepath)

    # Select threshold for normalization
    threshold, min_sample = get_reads_threshold(dataframe)
    print(f'Threshold selected {threshold} which is {min_sample}')

    # Set seed of NumPy random number generator to be reproducible
    numpy.random.seed(args.seed)

    # Normalize
    normalized_dataframe = normalize_data(dataframe, threshold)
    
    # Save result in the same folder, but with 'normalized_' prefix
    result_path = os.path.join(os.path.dirname(filepath), 'normalized_' + os.path.basename(filepath))
    dataloader.to_csv(normalized_dataframe, result_path)

if __name__ == u'__main__':
    normalize()
