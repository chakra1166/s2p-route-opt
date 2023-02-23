import pandas as pd
import numpy as np
import random
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.util.infeasible import log_infeasible_bounds, log_infeasible_constraints

random.seed(42)  # set the random seed for reproducibility


def route_value(model, route):
    return (0, 1)


def get_cost_df(model):
    total_cost = 0
    for route in model.route:
        total_cost = total_cost + model.route_value[route] * cost_dict[route]
    return total_cost


def cap_constraint(model, dc):
    cap_calc = 0
    for route in model.route:
        if route.split("_")[1] == dc:
            cap_calc = (
                cap_calc + model.route_value[route] * demand_dict[route.split("_")[0]]
            )
    return pyo.inequality(0, cap_calc, cap_dict[dc])


def demand_constraint(model, city):
    demand_calc = 0
    for route in model.route:
        if route.split("_")[0] == city:
            demand_calc = (
                demand_calc
                + model.route_value[route] * demand_dict[route.split("_")[0]]
            )
    return demand_calc == demand_dict[city]


def one_active_route(model, city):
    total_routes = 0
    for route in model.route:
        if route.split("_")[0] == city:
            total_routes = total_routes + model.route_value[route]
    return total_routes == 1


def prep_data(input_df):
    df = input_df.copy()
    df["x"] = 0
    df["city"] = df["state_name"] + "&" + df["city"]
    df["city_dc"] = df["city"] + "_" + df["DC"]
    df = df.drop_duplicates(subset="city_dc", keep="first")
    city_df = df[["city", "Demand"]].drop_duplicates()
    dc_df = df[["DC", "Capacity"]].drop_duplicates()
    return df, city_df, dc_df


# optimize routes
input_df = pd.read_csv("data/distance_matrix.csv")
df, city_df, dc_df = prep_data(input_df)
# Define the decision variables
route_dict = dict(zip(df.city_dc, df.x))
demand_dict = dict(zip(city_df.city, city_df.Demand))
cost_dict = dict(zip(df.city_dc, df["Cost"]))
cap_dict = dict(zip(dc_df.DC, dc_df.Capacity))

def run_optimizer(df):
    model = ConcreteModel(name="route_opt")
    # initialize set
    model.route = Set(initialize=df.city_dc, doc="routes")
    model.city = Set(initialize=city_df.city, doc="city")
    model.dc = Set(initialize=dc_df.DC, doc="dc")
    model.route_value = Var(
        model.route, initialize=route_dict, domain=Binary, bounds=(0, 1)
    )
    model.objective = Objective(rule=get_cost_df, sense=minimize)
    # Constraints
    model.max_cap = Constraint(model.dc, rule=cap_constraint)
    model.max_cap.activate()
    model.one_route = Constraint(model.city, rule=one_active_route)
    model.one_route.activate()
    opt = SolverFactory("glpk", executable="data\w64\glpsol")
    # Solving the pyomo model
    results = opt.solve(model)
    new_route_values = {k: value(v) for k, v in model.route_value.items()}
    df["route"] = df["city_dc"].map(new_route_values)
    df = df.loc[df["route"] == 1]
    if df.shape[0] == 0:
        raise Exception("Infeasible Soution - Try other values to simulate")
    return df

optimized_df = run_optimizer(df)

# input_df = pd.read_csv("data/distance_matrix.csv")


# df = input_df.copy()

# df["x"] = 0
# df["city"] = df["state_name"] + "&" + df["city"]

# # df = df.loc[df['city'].isin(df['city'].unique()[0:100])]


# df["city_dc"] = df["city"] + "_" + df["DC"]
# print(df.shape)
# df = df.drop_duplicates(subset="city_dc", keep="first")

# print(df.shape)
# df["Demand"] = df["Demand"]

# city_df = df[["city", "Demand"]].drop_duplicates()
# city_df

# dc_df = df[["DC", "Capacity"]].drop_duplicates()
# dc_df


# model = ConcreteModel(name="route_opt")

# # Define the decision variables
# route_dict = dict(zip(df.city_dc, df.x))
# demand_dict = dict(zip(city_df.city, city_df.Demand))
# cost_dict = dict(zip(df.city_dc, df["Cost"]))
# cap_dict = dict(zip(dc_df.DC, dc_df.Capacity))
# # initialize set
# model.route = Set(initialize=df.city_dc, doc="routes")
# model.city = Set(initialize=city_df.city, doc="city")

# model.dc = Set(initialize=dc_df.DC, doc="dc")
# # variables
# # model.route_value = Var(model.route, initialize=route_dict, within=Binary,bounds=route_value)
# model.route_value = Var(
#     model.route, initialize=route_dict, domain=Binary, bounds=(0, 1)
# )

# # Objective
# # minimize the cost objective
# model.objective = Objective(rule=get_cost_df, sense=minimize)


# # Constraints
# model.max_cap = Constraint(model.dc, rule=cap_constraint)
# model.max_cap.activate()

# # model.demand_meet = Constraint(model.city,rule = demand_constraint)
# # model.demand_meet.activate()

# model.one_route = Constraint(model.city, rule=one_active_route)
# model.one_route.activate()
# # Solver
# # opt = SolverFactory("bonmin")

# opt = SolverFactory("glpk", executable="C:\w64\glpsol")

# # Solving the pyomo model
# results = opt.solve(model)
# new_route_values = {k: value(v) for k, v in model.route_value.items()}
# df["route"] = df["city_dc"].map(new_route_values)


# def cap_constraint_validate(df):

#     for i in cap_dict.keys():

#         if df.loc[(df.DC == i) & (df.route == 1)]["Demand"].sum() > cap_dict[i]:
#             print(i)
#             print(df.loc[(df.DC == i) & (df.route == 1)]["Demand"].sum())
#             print("max : ", cap_dict[i])
#             print("#################")


# cap_constraint_validate(df)

# model.pprint()

