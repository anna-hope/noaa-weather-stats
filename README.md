# noaa-weather-stats

## introduction

This is a small tool that pulls NOAA data from 
`ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/by_year/`
and computes some summary statistics based on weather data from each year.

The question I wanted to answer by building this was
"for each of the core metrics given by NOAA (like avg temperature), can we see the top years"?

### details

NOAA provides the following core stats:

```
PRCP = Precipitation (tenths of mm)
SNOW = Snowfall (mm)
SNWD = Snow depth (mm)
TMAX = Maximum temperature (tenths of degrees C)
TMIN = Minimum temperature (tenths of degrees C)
```

as well as some others.

You can find more info at NOAA's [FTP server here](ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt),
along with a description of some of the other stats you might see in the output of this tool.

For example, I wanted to see what the top years were by average observed temperature or precipitation.


### running

#### Docker (recommended)

- docker build -t annahope/noaa-weather:0.1 .
- docker run -v /local/data/path/:/data annahope/noaa-weather:0.1
  --data-dir /data --year-start 2000

#### locally

- python3 -m pip install -r requirements.txt
- python3 runme.py --year-start 2000


### usage

```
usage: runme.py [-h] [--data-dir DATA_DIR] [--year-start YEAR_START]
                [--year-end YEAR_END] [--top-n-years TOP_N_YEARS]

optional arguments:
  -h, --help            show this help message and exit
  --data-dir DATA_DIR   path to store the NOAA data
  --year-start YEAR_START
                        first year for which to get the data
  --year-end YEAR_END   last year for which to get the data
  --top-n-years TOP_N_YEARS
                        how many years to output for each statistic
```

### sample output

(truncated)
for years 2000-2020

```
Computing means for every year
PRCP [2018, 2015, 2017, 2019, 2020]
SNOW [2011, 2019, 2014, 2013, 2018]
SNWD [2011, 2019, 2013, 2014, 2012]
TAVG [2003, 2015, 2002, 2014, 2001]
TMAX [2006, 2007, 2005, 2001, 2002]
TMIN [2006, 2005, 2007, 2001, 2003]
TOBS [2001, 2006, 2003, 2002, 2005]
```


### potential improvements

I'm not convinced that simply averaging something like TAVG for every weather station for the whole 
year is the most accurate way of calculating the total average temperature for the year. 

It would be great to find a more sophisticated way of computing these statistics, as well as
possibly correcting for missing data or outliers.

NOAA also provides geographical information for each of the weather stations in the data set. 
It might be cool to allow breaking up these stats by region.

It would also be cool to make some visualizations.

If anyone finds this useful, please let me know! Contributions are welcome :)