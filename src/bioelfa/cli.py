import logging
from pathlib import Path

from bioelfa._version import __version__
from bioelfa import normalizer, geneset_compare, dataloader
from bioelfa.dashboard import start_dashboard

from rich import print
import rich_click as click

click.rich_click.USE_RICH_MARKUP = True


@click.group()
def bioelfa():
    logging.basicConfig(level=logging.INFO)
    pass


@bioelfa.command()
def version():
    """Print version and exit."""
    print(f"Version: {__version__}")

@bioelfa.command(help=normalizer.normalize.__doc__)
@click.option(
    "-f",
    "--filepath",
    type=str,
    help="path to a csv file representing a gene reads table to normalize",
    required=True,
    default=None,
)
@click.option(
    "-s",
    "--seed",
    type=str,
    help="the seed used to initialize the random generator for the sampling operation. Defaults to 0",
    required=False,
    default=0,
)
def normalize(filepath: str, seed: int):
    dataframe = dataloader.load_csv(filepath)
    normalized_dataframe = normalizer.normalize(dataframe, seed)
    
    # Save result in the same folder, but with 'normalized_' prefix
    result_path = Path(filepath).parent / str('normalized_' + Path(filepath).name)
    dataloader.to_csv(normalized_dataframe, result_path)
    print(f"Normalized dataframe saved as CSV here: {result_path.absolute()} .")


@bioelfa.command(help=geneset_compare.compare_datasets.__doc__)
@click.option(
    "-f",
    "--filepath",
    type=str,
    help="path to a csv file with two datasets as columns with genes in AGI format.",
    required=True,
    default=None,
)
def compare(filepath: str):
    geneset_compare.compare_datasets(filepath)


@bioelfa.command()
@click.option(
    "-d",
    "--develop",
    type=bool,
    is_flag=True,
    help="Enables development mode on the dashboard, allowing to update the python package.",
    default=False,
)
def dashboard(develop: bool):
    """
    Start dashboard.
    """
    start_dashboard(develop=develop)


if __name__ == "__main__":
    bioelfa()
