import matplotlib.pyplot as plt
import numpy as np
import os, glob, time, json
from prm import prm
from prm_3D import prm_3D
from graph_3D import Graph3D
from graph import Graph
import copy
from data_fetcher import fetch_agent, fetch_static_obstacles, fetch_dynamic_obstacles
import data_algorithms as da
import data_plotter as dp
from sipp2 import sipp2
from sipp3 import sipp3

agent1 = fetch_agent("UnitOctagon")/2.0
agent2 = fetch_agent("UnitOctagon")/2.0
static_obstacles = fetch_static_obstacles("PolygonsSIPP")
dynamic_obstacles = fetch_dynamic_obstacles("LongRectangle", "Circular")
dilated_static_obstacles = da.dilate_obstacles(static_obstacles, res=2)

# Add dynamic obstacle constraints to second agent

def do_stuff(graph, path, agent):
	time = 20
	dt = 0.1
	i = 0
	t = 0
	new_dynamic_obstacle = dict()
	new_dynamic_obstacle["shape"] = agent
	new_dynamic_obstacle["pos"] = []
	while t < time:
		p, theta = da.find_current_pose_2(graph, path, t)
		new_agent = da.rigid_body_motion(agent, p, 0)
		new_dynamic_obstacle["pos"].append(new_agent)
		i += 1
		t += dt
	return new_dynamic_obstacle

# Saving graph:

filename1 = "./Graphs/graph_multi_1"
filename2 = "./Graphs/graph_multi_2"

graph1 = prm(dilated_static_obstacles, agent1, N=5000, k=4)
graph1.add_query_points((8, 1.5), (1.5, 8))
graph2 = prm(dilated_static_obstacles, agent2, N=5000, k=4)
graph2.add_query_points((1.5,8), (8, 1.5))

da.calculate_safe_intervals(graph1, dynamic_obstacles, agent1)
graph1.generate_new_nodes()

graph1.save_graph(filename1)
graph_res = copy.deepcopy(graph2)

# Opening graphs:

with open(filename1, "r") as f:
    data1 = json.loads(f.read())
    graph1 = Graph.deserialize(data1)

#with open(filename2, "r") as f:
#    data2 = json.loads(f.read())
#    graph2 = Graph.deserialize(data2)

fig1, ax1 = plt.subplots(1,1)
fig1.set_size_inches(10,10)
#dp.plot_graph(graph, ax1)
dp.plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax1, facecolor="black", buffercolor="white")

#plt.show()

PATHS = []
pbounds = [0.0001, 0.5, 0.9]
color_scheme = ["red", "blue", "green"]
i = 0
for pbound in pbounds:
    path1, total_cost1 = sipp3(graph1, pbound)
    dynamic_obstacles_multi = []
    dynamic_obstacles_multi.append(dynamic_obstacles)
    new_agent_as_dynamic_obstacle = do_stuff(graph1, path1, agent1)
    dynamic_obstacles_multi.append(new_agent_as_dynamic_obstacle)
    da.calculate_safe_intervals_multi(graph2, dynamic_obstacles_multi, agent2)
    graph2.generate_new_nodes()
    path2, total_cost2 = sipp3(graph2, pbound) 
    dp.plot_path(graph1, path1, ax1, color=color_scheme[i])
    dp.plot_path(graph2, path2, ax1, color=color_scheme[i])
    graph1 = Graph.deserialize(data1)
    graph2 = copy.deepcopy(graph_res)
    i += 1

circ = plt.Circle((5,4.5), radius=1, color='k', fill=False)
ax1.add_patch(circ)
plt.arrow(5,3.5,0.01,0,width=0.03, color='k')
start_agent = da.rigid_body_motion(agent1, (1.5,8), 0)
final_agent = da.rigid_body_motion(agent1, (8, 1.5), 0)
dp.plot_object(start_agent, ax1, color="black", alpha=0.5)
dp.plot_object(final_agent, ax1, color="black", alpha=0.5)
dp.plot_object(dynamic_obstacles["pos"][0], ax1, color="black", alpha=0.5)
plt.show()

#print("Time taken: " + str(t2-t1))#
#print(path)
#plan = da.path_to_plan(path, graph)
#print(plan)
#simulate_motion(graph, agent, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path, "Images", ax1)
