import logging

from bioelfa._version import __version__
from bioelfa import normalizer
from bioelfa import geneset_compare

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
    normalizer.normalize(filepath, seed)


@bioelfa.command(help=normalizer.normalize.__doc__)
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


if __name__ == "__main__":
    bioelfa()
