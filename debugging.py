import matplotlib.pyplot as plt
import numpy as np
import os, glob, time 
from prm import prm
from prm_3D import prm_3D
from graph_3D import Graph3D
from graph import Graph

from data_fetcher import fetch_agent, fetch_static_obstacles, fetch_dynamic_obstacles
from data_algorithms import dilate_obstacles, generate_bounding_box, rigid_body_motion, calculate_safe_intervals, calculate_safe_intervals_multi
from data_plotter import plot_graph, plot_object, plot_static_obstacles, plot_safe_intervals, make_video, simulate_motion, simulate_intervals, find_current_pose_2, simulate_motion_multi
from sipp2 import sipp2
from sipp3 import sipp3

agent = fetch_agent("UnitOctagon")/2
static_obstacles = fetch_static_obstacles("PolygonsSIPP")
dynamic_obstacles = fetch_dynamic_obstacles("UnitOctagon", "Circular")

dilated_static_obstacles = dilate_obstacles(static_obstacles, res=2)

t1 = time.time()
graph = prm(dilated_static_obstacles, agent, N=2000, k=4)
t2 = time.time()
print(t2-t1)

start_point = (8, 1.5)
end_point = (1.5, 8)
graph.add_query_points(start_point, end_point)
calculate_safe_intervals(graph, dynamic_obstacles, agent)
graph.generate_new_nodes()
path, total_cost = sipp3(graph)


fig1, ax1 = plt.subplots(1,1)
fig1.set_size_inches(10,10)
simulate_motion(graph, agent, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path, "Motion_Images", ax1)