import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import folium_static
from utils import get_folium_map, add_dc_markers, get_nearsest_dc, get_initial_map
from config import dc_lat_lng, dc_colors, capacity_grid_options, dc_capacity
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    JsCode,
    ColumnsAutoSizeMode,
)
from ui import header_ui, sidebar_ui

st.set_page_config(layout="wide")

# Function
# Read the optimized data
def load_optimized_df():
    opt_df = pd.read_csv("data/optimized_data.csv")
    st.session_state["optimal_df"] = opt_df
    return opt_df


# Header part
header_ui()
# Read the Distance Matrix Dataframe
input_df = pd.read_csv("data/distance_matrix.csv")
cur_df = get_nearsest_dc(input_df)
cur_capacity = cur_df.groupby(["DC"])["Demand"].sum().reset_index()
# Create Initial map based on distance
us_map = get_folium_map()
us_map = add_dc_markers(dc_lat_lng, dc_colors, us_map)
if "optimal_df" not in st.session_state:
    us_map = get_initial_map(cur_df, us_map)
else:
    opt_df = st.session_state["optimal_df"]
    # st.write(opt_df.type)
    us_map = get_initial_map(opt_df, us_map)
folium_static(us_map, width=900)

if st.session_state.get("optimal_df", None) is not None:
    sel_cols = [
        "city",
        "curr_DC",
        "DC",
        "user_input_dc",
        "Demand",
        "Cost Deviation",
        "lat",
        "lng",
    ]
    opt_df = st.session_state["optimal_df"]
    # opt_df = opt_df[sel_cols]
    gd2 = GridOptionsBuilder.from_dataframe(opt_df)
    gd2.configure_default_column(hide=True, editable=False)
    gd2.configure_column(field="city", header_name="Zone Name", hide=False)
    gd2.configure_column(field="curr_DC", header_name="Current DC", hide=False)
    gd2.configure_column(field="DC", header_name="Optimal DC", hide=False)
    gd2.configure_column(
        field="Demand", header_name="Total Orders", hide=False, editable=True
    )
    gd2.configure_column(
        field="Cost Deviation", header_name="Cost Deviation", hide=False
    )
    cs = JsCode(
        """
    function(params){
        if (params.data.user_input_dc != params.data.DC) {
            return {
                'backgroundColor' : '#FFCCCB'
        }
        }
    };
"""
    )

    editor_params = JsCode(
        """function(params) {
        var selectedCountry = params.data.country;
        if (['Excel', 'Vina'].includes(params.data.city)) {
            return {
                values: [
                    "Fresno",
                    "SLC",
                    "Olathe",
                    "Macon"
                ]
            };
        } else {
            return {
                values: [
                    "Fresno",
                    "SLC",
                    "Olathe",
                    "Indy",
                    "Hamburg",
                    "Macon",
                    "Charlotte",
                ]
            };
        }
    }"""
    )

    gd2.configure_column(
        field="user_input_dc",
        header_name="User Input DC",
        editable=True,
        cellStyle=cs,
        hide=False,
        cellEditor="agSelectCellEditor",
        cellEditorParams=editor_params,
    )
    grid_options2 = gd2.build()

    # section to add 4 metrics (dummy values)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Route Changes", 30)
    col2.metric("Current Cost", "$ 1,555")
    col3.metric("Optimal Cost", "$ 1,380", "11%", delta_color="inverse")
    col4.metric("Simulated Cost", "$ 1,450", "7%", delta_color="inverse")
    _, opt_col, _ = st.columns([1, 8, 1])
    with opt_col:
        # st.subheader("Optimal DC", )
        st.markdown(
            "<h2 style='text-align: center; color: black;'>Optimal DC Routes</h2>",
            unsafe_allow_html=True,
        )
        st.header("")

    optimal_df2 = AgGrid(
        opt_df,
        grid_options2,
        height=500,
        allow_unsafe_jscode=True,
        fit_columns_on_grid_load=True,
        theme="alpine",
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS
        # custome_css=custom_css,
    )["data"]

    optimal_df2["Color"] = optimal_df2["user_input_dc"].map(dc_colors)
    if not st.session_state["optimal_df"].equals(optimal_df2):
        st.session_state["optimal_df"] = optimal_df2
        st.experimental_rerun()

# Sidebar
with st.sidebar:
    sidebar_ui()
    tt = pd.DataFrame(dc_capacity)
    if "optimal_df" not in st.session_state:
        tt = pd.merge(tt, cur_capacity)
    else:
        opt_df = st.session_state["optimal_df"]
        cur_capacity = opt_df.groupby(["user_input_dc"])["Demand"].sum().reset_index()
        cur_capacity.columns = ["DC", "Demand"]
        tt = pd.merge(tt, cur_capacity)
    jscode = JsCode(
        """
    function(params) {
        if (params.data.Demand > params.data.Capacity) {
            return {
                'color': 'black',
                'backgroundColor': '#FFCCCB'
            }
        }
    };
    """
    )
    capacity_grid_options["getRowStyle"] = jscode
    grid_return = AgGrid(
        tt,
        capacity_grid_options,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
    )
    st.sidebar.button(label="Optimize", on_click=load_optimized_df)
    st.sidebar.file_uploader("Upload Custom Demand File", type=["csv", "excel"])
