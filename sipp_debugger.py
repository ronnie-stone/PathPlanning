import numpy as np
import matplotlib.pyplot as plt
import os 
import glob
from node import Node
from graph import Graph 
from prm import prm
from prm_oop import prm_oop
from fetch_static_obstacles import fetch_static_obstacles
from fetch_dynamic_obstacles import fetch_dynamic_obstacles
from fetch_agent import fetch_agent
from djikstra import djikstra
import time as tm
from sipp import sipp
from sipp2 import sipp2
from state import State

# Spatial functions:

from rigid_body_motion import rigid_body_motion
from calculate_safe_intervals import calculate_safe_intervals
from is_valid_pose import is_valid_pose

# Plotting functions for debugging:

from plot_graph import plot_graph
from plot_path import plot_path
from plot_static_obstacles import plot_static_obstacles
from plot_safe_intervals import plot_safe_intervals
from make_video import make_video

# First we remove whatever images we had before:

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
for filename in glob.glob(CURR_DIR + "/SafeIntervals/*.png"):
	os.remove(filename)

# First we fetch agent and obstacles data:

agent = fetch_agent("LongRectangle")
static_obstacles, dilated_static_obstacles = fetch_static_obstacles("PolygonsSIPP")
dynamic_obstacle = fetch_dynamic_obstacles("UnitOctagon", "Circular")

# We create a graph using PRM with the help of a KDTree:

graph = prm_oop(dilated_static_obstacles, agent, N = 10, k = 5)

# We add the two query points of interest:

state_1 = [2,0.5]
state_2 = [5,9]
start_index, end_index = graph.add_query_points(state_1, state_2)

# Now we must propagate the dynamic obstacle in time and define the safe intervals:
# We are using a time step of 0.1 units.

calculate_safe_intervals(graph, dynamic_obstacle, agent)

print("Original Nodes:")
for node in graph.nodes:
	print(node.index, node.x_pos, node.y_pos, node.safe_intervals)

print("Converted States")
# Now, for the real test, we try to implement A* and make sure it works:

fig, ax = plt.subplots(1,1)
fig.set_size_inches(18.5, 10.5)
plot_graph(graph, ax)
plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax)

path, cost = sipp2(graph)

print("Path Found:")
for index in path:
	print("Coordinates: " + str(graph.nodes[index].x_pos), str(graph.nodes[index].y_pos))
	print("Times: " + str(graph.nodes[index].time), str(graph.nodes[index].time2))

# Plotting section:

plot_path(graph, path, ax, agent=agent)
# plt.show()
'''
t3 = tm.time()

t = 0 
T = 10
dt = 0.1
i = 0

while t < T:
	plt.cla()
	plot_safe_intervals(graph, t, ax)
	plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax)
	step = '{:03d}'.format(i)
	plt.savefig("SafeIntervals/Step" + step)

	t += dt
	i += 1

t4 = tm.time()
print(t4-t3)

make_video("/SafeIntervals/*.png", "SafeIntervals")

#plot_graph(graph, ax)
#plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax)
# plot_path(graph, path, ax, agent=agent)

# plt.show()
'''