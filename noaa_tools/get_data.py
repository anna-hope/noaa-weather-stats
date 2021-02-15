import contextlib
from pathlib import Path
from typing import List
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen

from tqdm import tqdm

base_url = "ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/"


def get_data_ftp(url: str) -> bytes:
    # use contextlib so we have a prettier/nicer way of closing the stream for the downloaded file
    with contextlib.closing(urlopen(url)) as response:
        return response.read()


def download_data_for_year(year: int, data_path: Path) -> Path:
    # downloads the NOAA weather data for the given year
    # returns the number of bytes written to the local FS
    year_filename = f"{year}.csv.gz"
    file_path = Path(data_path, year_filename)
    if file_path.exists():
        return file_path

    year_url = urljoin(base_url, year_filename)
    year_data = get_data_ftp(year_url)

    with file_path.open("wb") as f:
        bytes_written = f.write(year_data)
        if bytes_written == 0:
            raise ValueError(
                f"couldn't get data for {year_filename}: got {bytes_written} bytes"
            )
    return file_path


def download_historical_data(
    *, year_start: int, year_end: int, data_path: Path = Path("data")
) -> List[Path]:
    # iterates over the range of year_start and year_end (inclusive)
    # and writes the data to the data path defined in global scope
    # in a real-life application, the output data path wouldn't be hardcoded

    # NB if the server throttles download speed for a client
    # then a possible improvement would be to use async coroutines instead
    # which should speed up the download

    years = range(year_start, year_end + 1)
    data_path.mkdir(exist_ok=True)

    # use tqdm to create a progress bar (NB sometimes doesn't work properly in jupyter)
    output_paths = []
    for year in tqdm(years):
        tqdm.write(f"getting data for {year}")
        file_path = download_data_for_year(year, data_path)
        output_paths.append(file_path)
    return output_paths
