import pandas as pd
import numpy as np
from config import dc_lat_lng, dc_capacity


cities_df = pd.read_csv("data/random_cities.csv")
sel_cols = ["state_name", "city", "lat", "lng"]
cities_df = cities_df[sel_cols]
# DC Dataframes
dc_df = pd.DataFrame.from_dict(dc_lat_lng, orient="index", columns=["dc_lat", "dc_lng"])
dc_df = dc_df.rename_axis("DC").reset_index()
dc_capacity = pd.DataFrame(dc_capacity)

df = pd.merge(cities_df, dc_df, how="cross")


def distance(s_lat, s_lng, e_lat, e_lng):
    # Approximate radius of earth in km
    R = 6373.0
    s_lat = s_lat * np.pi / 180.0
    s_lng = np.deg2rad(s_lng)
    e_lat = np.deg2rad(e_lat)
    e_lng = np.deg2rad(e_lng)
    d = (
        np.sin((e_lat - s_lat) / 2) ** 2
        + np.cos(s_lat) * np.cos(e_lat) * np.sin((e_lng - s_lng) / 2) ** 2
    )
    return 2 * R * np.arcsin(np.sqrt(d))


df["distance"] = distance(df["lat"], df["lng"], df["dc_lat"], df["dc_lng"])
df = pd.merge(df, dc_capacity, on="DC")

df["min_distance"] = df.groupby(["state_name", "city"])["distance"].transform("min")
df["dist_opt"] = np.where(df["distance"] == df["min_distance"], 1, 0)
# df["Demand_old"] = df["Demand"]
# df["Demand"] = (df["Demand"]*0.9).round(0)
# dfs=[]
# for state_name in df["state_name"].unique():
#     if state_name=="Washington":
#         tt = df.loc[df["state_name"]==state_name]
#         tt["dist_opt"] = np.where(tt["DC"]==tt["Fresno"],1,0)
#     elif state_name=="Oregon":
#         tt = df.loc[df["state_name"]==state_name]
#         tt["dist_opt"] = np.where(tt["DC"]==tt["Fresno"],1,0)

#     dfs.append(tt)
