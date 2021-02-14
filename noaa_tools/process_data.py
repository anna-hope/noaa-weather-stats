from datetime import datetime as dt, timedelta
from functools import partial
import gzip
import io
import os
from pathlib import Path

from joblib import Parallel, delayed
import pandas as pd


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

    df = df.loc[df.element_key.isin(common_keys)]

    # pivot the dataframe so that the values of element_key are columns
    df = df.pivot(
        index=["station_id", "date"], columns="element_key", values="element_value"
    )
    return df
