dc_lat_lng = {
    "Fresno": (36.74773, -119.77237),
    "SLC": (40.76078, -111.89105),
    "Olathe": (38.8814, -94.81913),
    "Indy": (39.997263, -86.345830),
    "Hamburg": (40.5009, -75.9699),
    "Macon": (32.84069, -83.6324),
    "Charlotte": (35.22709, -80.84313),
}

dc_capacity = {
    "DC": ["Fresno", "SLC", "Olathe", "Indy", "Hamburg", "Macon", "Charlotte"],
    "Capacity": [15_000, 2_500, 13_000, 12_000, 14_000, 22_000, 4_000],
}

dc_colors = {
    "Fresno": "red",
    "SLC": "blue",
    "Olathe": "green",
    "Indy": "purple",
    "Hamburg": "orange",
    "Macon": "pink",
    "Charlotte": "gray",
}

capacity_grid_options = {
    "defaultColDef": {"minWidth": 5},
    "columnDefs": [
        {"headerName": "DC", "field": "DC", "editable": False,},
        {"headerName": "Capacity", "field": "Capacity", "editable": True,},
        {"headerName": "Demand", "field": "Demand", "editable": True,},
    ],
}
