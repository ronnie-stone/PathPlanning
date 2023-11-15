# This test is concerned with propagating dynamic obstacles and seeing its 
# impact in the configuration space of the object travelling.

# Python standard libraries:

import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import os

# Our implementations of common path-planning algorithms:

from prm import prm
from djikstra import djikstra

# Plotting functions:

from plot_static_obstacles import plot_static_obstacles
from plot_graph import plot_graph
from plot_path import plot_path

# Auxiliary functions:

from pick_endpoints import pick_endpoints
from remove_nodes import remove_nodes
from restore_nodes import restore_nodes
from make_video import make_video
from fetch_agent import fetch_agent
from fetch_static_obstacles import fetch_static_obstacles
from fetch_dynamic_obstacles import fetch_dynamic_obstacles
from rigid_body_motion import rigid_body_motion
from generate_patch import generate_patch
from is_valid_point import is_valid_point

if __name__ == "__main__":

	#CURR_DIR = os.path.dirname(os.path.realpath(__file__))
	#for filename in glob.glob(CURR_DIR + "/test7/*.png"):
	#	 os.remove(filename)

	agent = fetch_agent("LongRectangle")
	static_obstacles, dilated_static_obstacles = fetch_static_obstacles("PolygonsSIPP")
	dynamic_obstacles = fetch_dynamic_obstacles("LongRectangle", "Circular")

	t1 = time.time()

	graph_prm, x_array_prm, y_array_prm = prm(dilated_static_obstacles, agent, N=1000, k=6)

	t2 = time.time()

	print(t2-t1)

	goal = (7,9)
	start = (2, 0.5)
	i = 0
	t = 0
	T = 10
	dt = 0.1
	speed = 0.2

	t3 = time.time()
	qinit, qgoal = pick_endpoints((start[0], start[1]), (goal[0], goal[1]), x_array_prm, y_array_prm)
	t4 = time.time()

	print(t4 - t3)

	'''

	fig, [ax1, ax2] = plt.subplots(1,2)
	fig.set_size_inches(18.5, 10.5)

	x_trajectory = [x_array_prm[qinit]]
	y_trajectory = [y_array_prm[qinit]]

	while t < T - dt:

		plt.sca(ax1)
		plt.cla()
		plt.sca(ax2)
		plt.cla()

		translated_agent1 = rigid_body_motion(dynamic_obstacles["shape"],
		[dynamic_obstacles["xpos"][min([i,99])], dynamic_obstacles["ypos"][min([i,99])]], 0)

		invalid_nodes = remove_nodes(graph_prm, x_array_prm, y_array_prm, [translated_agent1], agent)
		path_prm, total_cost = djikstra(qinit, qgoal, graph_prm, x_array_prm, y_array_prm, astar=True)
		qinit, qgoal = pick_endpoints((start[0], start[1]), (goal[0], goal[1]), x_array_prm, y_array_prm)

		x_cur = x_trajectory[i]
		y_cur = y_trajectory[i]

		if not path_prm:
			x_trajectory.append(x_cur)
			y_trajectory.append(y_cur)
		else:
			x0 = (x_array_prm[path_prm[0]], y_array_prm[path_prm[0]])
			x1 = (x_array_prm[path_prm[1]], y_array_prm[path_prm[1]])
			theta = np.arctan2(x1[1] - x0[1], x1[0] - x0[0])
			dx = speed*np.cos(theta)
			dy = speed*np.sin(theta)
			x_cur += dx
			y_cur += dy
			x_trajectory.append(x_cur)
			y_trajectory.append(y_cur)

		# Left plot:

		plt.sca(ax1)

		qinit, qgoal = pick_endpoints((x_cur, y_cur), (goal[0], goal[1]), x_array_prm, y_array_prm)
		translated_agent2 = rigid_body_motion(agent, [x_cur, y_cur], 0)

		patch1 = generate_patch(translated_agent1, facecolor="green")
		patch2 = generate_patch(translated_agent2, facecolor="yellow")
		ax1.add_patch(patch1)
		ax1.add_patch(patch2)
		plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax1)

		# Right Plot:

		plt.sca(ax2)

		for j in range(len(x_array_prm)):
			if j in invalid_nodes:
				ax2.plot(x_array_prm[j], y_array_prm[j], "ro", markersize=3)
			else:
				ax2.plot(x_array_prm[j], y_array_prm[j], "go", markersize=3)

		ax2.set_aspect(1)
		plt.tick_params(left=False,bottom=False)
		plt.xticks(color='w')
		plt.yticks(color='w')
		plt.axis([0, 10, 0, 10])
		plot_path(path_prm, x_array_prm, y_array_prm, "b", ax2, legend=False)

		step = '{:03d}'.format(i)

		plt.savefig("test7/Step" + step)

		i += 1
		t += dt

		print("Current time: " + str(t))
		print("Iteration no: " + str(i))

		restore_nodes(graph_prm, x_array_prm, y_array_prm)

		if np.sqrt((x_cur-goal[0])**2 + (y_cur-goal[1])**2) < 0.2:
			print("Script terminated!")
			break 

	make_video("/test7/*.png", "test7")

	'''
