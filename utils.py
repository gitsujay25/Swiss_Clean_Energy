import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
import json


#------------------- load_data -------------------------
# This function loads the csv data to a pandas DataFrame
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

#------------------- load_geojsn_data -------------------------
# This function loads the geojson data 
@st.cache_data
def load_geojsn_data(file):
    with open(file) as response:
        df  = json.load(response)
    return df

#------------------- load_geopanda_data -------------------------
# This function loads the geojson data to a geopanda file
@st.cache_data
def load_geopanda_data(file):
    df = gpd.read_file(file)
    return df

#------------------- give_catag -------------------------
# This function takes a pandas DataFrame and first filters
# the data for with a column col whose value is filter
# then it groups the data by cantons and returns the 
# grouped DataFrame
def give_catag(df, col, filter):
    subset=df[df[col]==filter]
    df_out=subset.groupby('canton_name').size().reset_index(name='count')
    return df_out

#------------------- give_catag2 -------------------------
# This function takes a pandas DataFrame and first filter
# the data for with a column col whose value is filter
# and returns the filtered DataFrame
def give_catag2(df, col, filter):
    df_out=df[df[col]==filter]
    return df_out

#------------------- give_cntr_zoom -------------------------
# This function returns the latitude and longitude at the
# center and also returns the zoom value needed for plotly
# chloropeth map for a selected canton
def give_cntr_zoom(df,col,filter):
    df_tmp = df[df[col]==filter]
    #df_tmp.geometry.bounds.minx.to_list()
    lon_limit = [df_tmp.geometry.bounds.minx.to_list()[0], df_tmp.geometry.bounds.maxx.to_list()[0]]
    lat_limit = [df_tmp.geometry.bounds.miny.to_list()[0], df_tmp.geometry.bounds.maxy.to_list()[0]]
    lon_center= (lon_limit[0]+lon_limit[1])/2
    lat_center= (lat_limit[0]+lat_limit[1])/2
    lat_bound = abs(lat_limit[0]-lat_limit[1])
    lon_bound = abs(lon_limit[0]-lon_limit[1])
    xx = max(lon_bound, lat_bound)
    zoom = 7.8 + 3.2*np.log10(1/xx)
    return lat_center, lon_center, zoom