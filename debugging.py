import matplotlib.pyplot as plt
import numpy as np
import os, glob, time, json
from prm import prm
from prm_3D import prm_3D
from graph_3D import Graph3D
from graph import Graph

from data_fetcher import fetch_agent, fetch_static_obstacles, fetch_dynamic_obstacles
import data_algorithms as da
import data_plotter as dp
from sipp2 import sipp2
from sipp3 import sipp3

agent = fetch_agent("UnitOctagon")/2
#agent = fetch_agent("LongRectangle")
static_obstacles = fetch_static_obstacles("PolygonsSIPP")
dynamic_obstacles = fetch_dynamic_obstacles("LongRectangle", "Circular")
dilated_static_obstacles = da.dilate_obstacles(static_obstacles, res=2)

# Saving graph:

# filename = "./Graphs/graph_10000_8_BIG"
filename = "./Graphs/graph_10000_8_CR"

#graph = prm(dilated_static_obstacles, agent, N=10000, k=8)
#graph.add_query_points((8, 1.5), (1.5, 8))
#da.calculate_safe_intervals(graph, dynamic_obstacles, agent)
#graph.generate_new_nodes()
#graph.save_graph(filename)

# Opening graph:
with open(filename, "r") as f:
    data = json.loads(f.read())
    graph = Graph.deserialize(data)

fig1, ax1 = plt.subplots(1,1)
fig1.set_size_inches(10,10)
#dp.plot_graph(graph, ax1)
dp.plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax1, facecolor="black", buffercolor="white")
#plt.show()


PATHS = []
pbounds = [0.99]
plans = []
color_scheme = ["red", "blue", "gold", "magenta", "green", "cyan"]
i = 0
for pbound in pbounds:
    path, total_cost = sipp3(graph, pbound)
    plan = da.path_to_plan(path, graph)
    plans.append(plan)
    dp.plot_path(graph, path, ax1, color=color_scheme[i])
    graph = Graph.deserialize(data)
    i += 1
circ = plt.Circle((5,4.5), radius=1, color='k', fill=False)
ax1.add_patch(circ)
plt.arrow(5,3.5,0.01,0,width=0.03, color='k')
start_agent = da.rigid_body_motion(agent, (1.5,8), 0)
final_agent = da.rigid_body_motion(agent, (8, 1.5), 0)
dp.plot_object(start_agent, ax1, color="black", alpha=0.5)
dp.plot_object(final_agent, ax1, color="black", alpha=0.5)
dp.plot_object(dynamic_obstacles["pos"][0], ax1, color="black", alpha=0.5)
plt.show()
for i in plans:
    print(plan)

# Need to write a Monte Carlo simulator here:


#dp.simulate_motion(graph, agent, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path, "Images", ax1)