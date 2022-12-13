import pandas as pd


# -----------------------------------------------------------------------------
# Using raw data as starting point
# -----------------------------------------------------------------------------
df = pd.read_pickle("../../data/raw/air-quality-index.pickle")
print(f"Data first rows before treatment:\n {df.head(10)}\n\n")
print(f"Dataset info:\n {df.info()}\n")

# -----------------------------------------------------------------------------
# Dealing with duplicates
# -----------------------------------------------------------------------------
# Check duplication of df excluding geo_shape and geo_point_2d
df.duplicated(df.columns.difference(["geo_shape", "geo_point_2d"])).sum()

# I used to get 817 duplicates but not anymore. Keeping the code just in case it happens again.
df.duplicated(
    [
        "date_ech",
        "date_dif",
        "code_zone",
        "lib_zone",
        "code_qual",
        "lib_qual",
        "coul_qual",
        "source",
        "type_zone",
        "code_no2",
        "code_so2",
        "code_o3",
        "code_pm10",
        "code_pm25",
        "x_wgs84",
        "y_wgs84",
        "x_reg",
        "y_reg",
        "epsg_reg",
    ]
).sum()

df.duplicated(
    [
        "date_ech",
        "date_dif",
        "code_zone",
        "lib_zone",
        "code_qual",
        "lib_qual",
        "coul_qual",
        "source",
        "type_zone",
        "code_no2",
        "code_so2",
        "code_o3",
        "code_pm10",
        "code_pm25",
        "x_wgs84",
        "y_wgs84",
        "x_reg",
        "y_reg",
        "epsg_reg",
        "objectid",
    ]
).sum()

# Removing objectid column
df.drop(columns=["objectid"], inplace=True)

# Converting **geo_shape** and **geo_point_2d** to string
df["geo_shape"] = df.geo_shape.astype(str)
df["geo_point_2d"] = df.geo_point_2d.astype(str)

print(f"Duplicates before rows: {df.duplicated().sum()}")
df.drop_duplicates(inplace=True)
print(f"Duplicates rows after: {df.duplicated().sum()}")


# -----------------------------------------------------------------------------
# Removing and rearranging columns
# -----------------------------------------------------------------------------
# Removing
columns_to_drop = [
    "coul_qual",
    "date_dif",
    "source",
    "type_zone",
    "code_zone",
    "x_wgs84",
    "y_wgs84",
    "x_reg",
    "y_reg",
    "epsg_reg",
    "geo_shape",
    "geo_point_2d",
]
df.drop(
    columns=columns_to_drop,
    errors="ignore",
    inplace=True,
)
print(f"Removed columns: {columns_to_drop}")

# Renaming
cols = [
    "date",
    "quality_code",
    "quality_label",
    "city",
    "no2",
    "so2",
    "o3",
    "pm10",
    "pm2-5",
    "zip_code",
]
df.columns = cols
print(f"Renamed columns: {cols}")

# Moving
city = df.pop("city")
df.insert(1, "city", city)
del city

zip_code = df.pop("zip_code")
df.insert(2, "zip_code", zip_code)
del zip_code

quality_label = df.pop("quality_label")
df.insert(3, "quality_label", quality_label)
del quality_label
print("Columns moved")

# -----------------------------------------------------------------------------
# Replacing incorrect
# -----------------------------------------------------------------------------
pollutants = ["no2", "so2", "o3", "pm10", "pm2-5"]
for p in pollutants:
    df[p] = df[p].replace(0, 1)
print("Zero values treated")

# -----------------------------------------------------------------------------
# Converting dtypes
# -----------------------------------------------------------------------------
# lower cases
df["quality_label"] = df["quality_label"].str.lower()
df["city"] = df["city"].str.lower()

# Convert date
df["date"] = pd.to_datetime(df["date"]).dt.date
df["date"] = pd.to_datetime(df["date"]).dt.normalize()

print("Conversions done")

# -----------------------------------------------------------------------------
# Enriching data
# -----------------------------------------------------------------------------
# Using index since date column is my index
df["year"] = pd.DatetimeIndex(df.date).year
df["month"] = pd.DatetimeIndex(df.date).month
df["day"] = pd.DatetimeIndex(df.date).day
df["weekday"] = pd.DatetimeIndex(
    df.date
).weekday  # The day of the week with Monday=0, Sunday=6.
df["week_of_year"] = df.date.dt.isocalendar().week
print("Data enriched")

# -----------------------------------------------------------------------------
# Sorting data
# -----------------------------------------------------------------------------
# Sorting  by date then city
df.sort_values(by=["date", "city"], inplace=True)
# Multi-index dataframe
df = df.set_index(["city", "date"]).sort_index()
print("Data sorted")

print(f"Data first rows after treatment:\n {df.head(10)}\n\n")
print(f"Dataset info:\n {df.info()}")


# -----------------------------------------------------------------------------
# Generating files
# -----------------------------------------------------------------------------
df.to_csv("..\\..\\data\\processed\\air-quality-index.csv", index=True)
df.to_pickle("..\\..\\data\\processed\\air-quality-index.pickle")
