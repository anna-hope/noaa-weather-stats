from argparse import ArgumentParser
from datetime import datetime as dt, timedelta

from noaa_tools import get_data

cur_year = dt.now().year

arg_parser = ArgumentParser()
arg_parser.add_argument(
    "--year-start",
    type=int,
    default=1990,
    help="first year for which to get the data",
)
arg_parser.add_argument(
    "--year-end",
    type=int,
    default=cur_year - 1,
    help="last year for which to get the data",
)
args = arg_parser.parse_args()
