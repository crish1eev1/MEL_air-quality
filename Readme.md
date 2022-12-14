# Generating automated reports on Lille Metropole air quality
-----------
This Python script calls https://opendata.lillemetropole.fr API to get air quality data from their "indice-qualite-de-lair" dataset and generates automated reports for each city.


## Project Organization
    ├── README.md                   <- You are here.
    ├── data
    │   ├── raw                     <- Extracted data gets uploaded here in the form of csv and pickle file
    │   └── processed               <- Clean data with air quality index and air pollutants details per city
    │
    ├── notebooks                   <- Draft stuff
    │    │
    ├── reports                     <- Generated html reports
    │   └── figures                 <- Generated graphics and figures
    │
    ├── requirements.txt            <- The requirements file for reproducing the environment
    │
    └── src                         <- Source code for use in this project.
        ├── data                    
        │   └── extract_data.py     <- Script to extract the data from this 'very well-known site' and generate csv files in data/raw
        │   └── transform_data.py   <- Script to transform csv files from data/raw to interim and processed files
        │
        └── visualization           
            └── visualize.py        <- Scripts to create visualizations


## Description
The data retrieved from "indice-qualite-de-lair" Lille Metropole dataset is actually originating from Atmo HDF. 

It contains data from 1st January 2022 for the 95 cities of the European Metropolis of Lille. It is composed of a daily main indicator as well as 5 sub-indices, each representative of an air pollutant:
- Nitrogen dioxide (no2) 
- Sulfur dioxide (so2) 
- Ozone (o3) 
- Particulate Matter of of less than 10mm (pm10)
- Particulate Matter of of less than 2.5mm (pm2-5) 

The highest sub-index determines the index of the day. For example, if all indexes are at 1 (good) except one that is at 4 (Poor), the general index will be at 4.


## Technology
Python and its various libraries:
- `pandas` to manipulate data
- `numpy` to work with arrays etc.
- `matplotlib.pyplot` to create and customize visualizations
etc.


## Limitations

- The level of granularity of the data is quite poor. In an ideal world I would have had access to the raw data of the measurements instead of their sub-indexes. With the data I've worked with, I'm not able to differentiate a 51 µg/m3 Particulate Matter 10 from a 100 µg/m3 measurement for example. They would both fold into the "Poor" category despite being quite different from each others. 
- I only get data from 01/01/2022 from this source of data


## Indexes 

| O3          | SO2        | NO2        | PM10       | PM2.5    | Level              |
|-------------|------------|------------|------------|----------|---------------------|
| 0 to 50     | 0 to 100   | 0 to 40    | 0 to 20    | 0 to 10  | Good                |
| 50 to 100   | 100 to 200 | 40 to 90   | 20 to 40   | 10 to 20 | Fair                |
| 100 to 130  | 200 to 350 | 90 to 120  | 40 to 50   | 20 to 25 | Moderate            |
| 130 to 240  | 350 to 500 | 120 to 230 | 50 to 100  | 25 to 50 | Poor                |
| 240 to 380  | 500 to 750 | 230 to 340 | 100 to 150 | 50 to 75 | Very Poor           |
| > 380       | > 750      | > 340      | > 150      | > 75     | Extremely Poor      |	 


## License
This project is open-source and available under the [MIT License](https://choosealicense.com/licenses/mit/). 