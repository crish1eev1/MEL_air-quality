import requests
import pandas as pd

import pickle

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------
dataset_id = "indice-qualite-de-lair"
format = "json"
limit = 10
test_link = f"https://opendata.lillemetropole.fr/api/v2/catalog/datasets/{dataset_id}/exports/{format}?limit={limit}"
limit = "-1"  # argument to pass to get the full dataset
link = f"https://opendata.lillemetropole.fr/api/v2/catalog/datasets/{dataset_id}/exports/{format}?limit={limit}"


# -----------------------------------------------------------------------------
# Verifying API response
# -----------------------------------------------------------------------------
r = requests.get(test_link, timeout=2)
print(f"URL: {r.url}")
print(f"HTTP Response Status Code: {r.status_code}")
print(f"HTTP Error: {r.raise_for_status()}")
print(f"Encoding: {r.encoding}")
print(f"Header content type: {r.headers.get('content-type')}")
print(f"Cookies: {r.cookies}")
r.close()
# -----------------------------------------------------------------------------
# Extracting data
# -----------------------------------------------------------------------------
df = pd.read_json(link)
print("dataframe created")
# Generating csv
df.to_csv("..\\..\\data\\raw\\air-quality-index.csv", index=False)
df.to_pickle("..\\..\\data\\raw\\air-quality-index.pickle")
print("dataframe saved")
