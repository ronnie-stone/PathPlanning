import matplotlib.pyplot as plt
import numpy as np
import os, glob, time 
from prm import prm
from prm_3D import prm_3D
from graph_3D import Graph3D

# Custom Modules:

from data_fetcher import fetch_agent, fetch_static_obstacles, fetch_dynamic_obstacles
from data_algorithms import dilate_obstacles, generate_bounding_box, rigid_body_motion, calculate_safe_intervals, calculate_safe_intervals_multi
from data_plotter import plot_graph, plot_object, plot_static_obstacles, plot_safe_intervals, make_video, simulate_motion, simulate_intervals, find_current_pose_2, simulate_motion_multi
from sipp2 import sipp2

def do_stuff(graph, path, agent):
	time = 20
	dt = 0.1
	i = 0
	t = 0
	new_dynamic_obstacle = dict()
	new_dynamic_obstacle["shape"] = agent
	new_dynamic_obstacle["pos"] = []
	while t < time:
		p, theta = find_current_pose_2(graph, path, t)
		new_agent = rigid_body_motion(agent, p, 0)
		new_dynamic_obstacle["pos"].append(new_agent)
		i += 1
		t += dt
	return new_dynamic_obstacle

# Data Fetching & Manipulation (Reviewed):

agent_1 = fetch_agent("UnitOctagon")/2
agent_2 = fetch_agent("UnitOctagon")/2
static_obstacles = fetch_static_obstacles("PolygonsSIPP")
dynamic_obstacles = fetch_dynamic_obstacles("Print", "Constant")
dilated_static_obstacles = dilate_obstacles(static_obstacles, res=2)
start_point_1 = (8, 1.5)
end_point_1 = (1.5, 8)
start_point_2 = (1.5, 8)
end_point_2 = (8,1.5)
new_agent_1 = rigid_body_motion(agent_1, start_point_1, 0)


graph_1 = prm(dilated_static_obstacles, agent_1, N=2000, k=6)
fig1, ax1 = plt.subplots(1,1)
fig1.set_size_inches(10,10)
graph_1.add_query_points(start_point_1, end_point_1)
#calculate_safe_intervals(graph_1, dynamic_obstacles, agent_1)
#graph_1.generate_new_nodes()


#t0 = time.time()
#path1, total_cost1 = sipp2(graph_1)
#print(path1, total_cost1)
#t1 = time.time()
#t_path_1 = t1-t0
#print("Finding Path: " + str(t_path_1))


plot_graph(graph_1, ax1)
plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax1)
plot_object(new_agent_1, ax1)
#graph_2 = prm(dilated_static_obstacles, agent_2, N=3000, k=6)
#graph_2.add_query_points(start_point_2, end_point_2)
#dynamic_obstacles_multi = []
#dynamic_obstacles_multi.append(dynamic_obstacles)
#new_agent_as_dynamic_obstacle = do_stuff(graph_1, path1, agent_1)
#dynamic_obstacles_multi.append(new_agent_as_dynamic_obstacle)
#calculate_safe_intervals_multi(graph_2, dynamic_obstacles_multi, agent_2)
#graph_2.generate_new_nodes()

#t0 = time.time()
#path2, total_cost2 = sipp2(graph_2)
#print(path2, total_cost2)
#t1 = time.time()
#t_path_2 = t1-t0
#print("Finding Path: " + str(t_path_2))

#plot_graph(graph, ax2)
#plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax2)
plt.show()
# simulate_intervals(graph, static_obstacles, dilated_static_obstacles, dynamic_obstacles, "Safe_Interval_Images", ax)
# simulate_motion_multi(graph_1, graph_2, agent_1, agent_2, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path1, path2, "Motion_Images", ax1)
#simulate_motion(graph_1, agent_1, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path, "Motion_Images", ax1)