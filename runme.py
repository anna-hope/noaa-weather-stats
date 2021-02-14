#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime as dt, timedelta

from noaa_tools import get_data, process_data

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


def main():
    print("Getting the data...")
    data_paths = get_data.download_historical_data(args.year_start, args.year_end)
    print("Computing means for every year")
    df_means_years = process_data.get_means_noaa_files(data_paths)
    print(df_means_years.idxmax())


if __name__ == "__main__":
    main()
