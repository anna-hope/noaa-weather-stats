#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime as dt
from pathlib import Path

from noaa_tools import get_data, process_data

cur_year = dt.now().year

arg_parser = ArgumentParser()
arg_parser.add_argument(
    "--data-dir", type=Path, default=Path("data"), help="path to store the NOAA data"
)
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
arg_parser.add_argument(
    "--top-n-years",
    type=int,
    default=5,
    help="how many years to output for each statistic",
)
args = arg_parser.parse_args()


def main():
    print("Getting the data...")
    data_paths = get_data.download_historical_data(
        year_start=args.year_start, year_end=args.year_end, data_path=args.data_dir
    )
    print("Computing means for every year")
    df_means_years = process_data.get_means_noaa_files(data_paths)
    for column_name in df_means_years.columns:
        sorted_years = df_means_years.sort_values(
            column_name, ascending=False
        ).index.tolist()
        top_sorted_years = sorted_years[: args.top_n_years]
        print(column_name, top_sorted_years)


if __name__ == "__main__":
    main()
