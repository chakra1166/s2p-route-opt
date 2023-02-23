import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static


def get_folium_map():
    # Create base map
    m = folium.Map(location=[40, -95], zoom_start=4.4)
    # Create USA map
    # Add choropleth to the map
    folium.Choropleth(
        geo_data="./data/us-state-boundaries.geojson",
        line_opacity=0.8,
        fill_color="yellow",
        fill_opacity=0.1,
        highlight=True,
    ).add_to(m)
    return m


def add_dc_markers(dc_lat_lng, dc_colors, folium_map):
    for dc_name, (lat, long) in dc_lat_lng.items():
        folium.Marker(
            [lat, long],
            popup=dc_name,
            tooltip=dc_name,
            icon=folium.map.Icon(
                color=dc_colors.get(dc_name), icon="industry", prefix="fa",
            ),
        ).add_to(folium_map)
    return folium_map


def add_cities(city, lat, lng, dc, colors, folium_map):
    for city, lat, lng, dc, clr in zip(city, lat, lng, dc, colors):
        folium.CircleMarker(
            [lat, lng],
            radius=17,
            fill=True,
            fill_color=clr,
            color=False,
            fill_opacity=0.3,
            tooltip=f"Zone:{city}, Optimal:{dc}",
        ).add_to(folium_map)
    return folium_map


def add_cities_opt(city, lat, lng, opt_dc, curr_dc, colors, folium_map):
    for city, lat, lng, opt_dc, curr_dc, clr in zip(
        city, lat, lng, opt_dc, curr_dc, colors
    ):
        folium.CircleMarker(
            [lat, lng],
            radius=17,
            fill=True,
            fill_color=clr,
            color=False,
            fill_opacity=0.3,
            tooltip=f"Zone:{city}, Recommended:{opt_dc}, Optimal: {curr_dc}",
        ).add_to(folium_map)
    return folium_map


def get_initial_map(df, folium_map):
    cities = df["city"].values.tolist()
    lat = df["lat"].values.tolist()
    lng = df["lng"].values.tolist()
    dc = df["DC"].values.tolist()
    colors = df["Color"].values.tolist()
    folium_map = add_cities(cities, lat, lng, dc, colors, folium_map)
    return folium_map


def get_initial_map_opt(df, folium_map):
    cities = df["city"].values.tolist()
    lat = df["lat"].values.tolist()
    lng = df["lng"].values.tolist()
    dc = df["DC"].values.tolist()
    curr_dc = df["curr_DC"].values.tolist()
    colors = df["Color"].values.tolist()
    folium_map = add_cities_opt(cities, lat, lng, dc, curr_dc, colors, folium_map)
    return folium_map


def get_nearsest_dc(df):
    # tt = df.sort_values(by=["city", "distance"], ascending=True)
    # tt = df.groupby(["city"]).head(1)
    tt = df.loc[df["dist_opt"] == 1]
    return tt

