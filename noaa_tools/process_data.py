from datetime import datetime as dt, timedelta
import os
from pathlib import Path
from typing import Dict, List

from joblib import Parallel, delayed
import pandas as pd

# (from NOAA) The five core elements are:
# PRCP = Precipitation (tenths of mm)
# SNOW = Snowfall (mm)
# SNWD = Snow depth (mm)
# TMAX = Maximum temperature (tenths of degrees C)
# TMIN = Minimum temperature (tenths of degrees C)

core_keys = {"PRCP", "SNOW", "SNWD", "TMAX", "TMIN"}


def read_noaa_data(data_file: Path) -> pd.DataFrame:
    # per ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
    # 1. is weather station id
    # 2. is date data was collected
    # 3. is a key for a piece of data
    # 4. is the value
    # 5-9 are extra flags for "quality"/source of data
    # which i assume for now i don't need

    # so we need to just use the first 3
    cols_to_use = list(range(0, 4))
    columns = ["station_id", "date", "element_key", "element_value"]

    df = pd.read_csv(data_file, usecols=cols_to_use, header=0, names=columns)
    # let's assume that values that occur less than 5% of the time
    # are too rare to be useful
    # possible improvement: some more sophisticated heuristics
    # based on the keys/values that tend to be given by individual weather stations

    key_counts = df.element_key.value_counts(normalize=True)
    common_keys = key_counts[key_counts > 0.05]
    common_keys = common_keys.index

    # but the core keys should always be there
    if not core_keys.issubset(common_keys):
        raise ValueError(f"The dataframe is missing the core keys {core_keys}")

    df = df.loc[df.element_key.isin(common_keys)]

    # pivot the dataframe so that the values of element_key are columns
    df = df.pivot(
        index=["station_id", "date"], columns="element_key", values="element_value"
    )
    return df


def compute_means(df: pd.DataFrame) -> pd.DataFrame:
    # get the year
    # the dataframe's index is a MultiIndex in the format
    # (station_id, yyyymmdd)
    df_first_timestamp = df.index[0][1]
    df_year = dt.strptime(str(df_first_timestamp), "%Y%m%d").year

    summary_stats: Dict[str, float] = df.mean().to_dict()
    for key, value in summary_stats.items():
        # temperatures are given in tenths of degrees C
        # so to convert them to regular C we need to /10
        if key.startswith("T"):
            summary_stats[key] = value / 10

    df_summary = pd.DataFrame(summary_stats, index=[df_year])
    return df_summary


def get_means_df_file(data_file: Path) -> pd.DataFrame:
    df = read_noaa_data(data_file)
    df_means = compute_means(df)
    return df_means


def get_means_noaa_files(data_files: List[Path] = None) -> pd.DataFrame:
    if not data_files:
        data_dir = Path("data")
        data_files = [item for item in data_dir.iterdir() if ".csv" in item.suffixes]

    # don't overload the machine -- only use half + 1 of all available CPUs
    max_cpus = os.cpu_count() // 2 + 1
    dfs_means = Parallel(n_jobs=max_cpus)(
        delayed(get_means_df_file)(data_file) for data_file in data_files
    )
    df_means_combined = pd.concat(dfs_means)
    return df_means_combined
