import matplotlib.pyplot as plt
from rigid_body_motion import rigid_body_motion
from generate_patch import generate_patch


def plot_path(graph, path, ax, legend=False, agent=[], t_array=[]):
	"""
	Plots the path generated.

		Parameters:

		graph (Graph object): See class definition for information.
		path (N x 1 float array): Node indices that make up the path found.
		ax (Matplotlib object): Axis to be plotted on.

		Returns:

		None

	"""

	# If path is empty, do not plot anything:

	if not path:
		return 

	plt.sca(ax)
	nodes = graph.nodes
	path_length = len(path)

	poses=False
	if len(agent) > 0:
		poses = True

	orientation = False
	if len(t_array) > 0:
		orientation = True

	for i in range(path_length - 1):

		node_1 = nodes[path[i]]
		node_2 = nodes[path[i+1]]
		plt.plot([node_1.x_pos, node_2.x_pos], [node_1.y_pos, node_2.y_pos],
		color="blue", alpha=1.0, zorder=3, lw=3.0)

		if poses:
			if orientation:
				translated_agent = rigid_body_motion(agent, [node_1.x_pos, node_1.y_pos], t_array[k2])
			else:
				translated_agent = rigid_body_motion(agent, [node_1.x_pos, node_1.y_pos], 0)
			patch = generate_patch(translated_agent, facecolor="green", alpha=0.5)
			ax.add_patch(patch)

	if poses:
		translated_agent = rigid_body_motion(agent, [node_2.x_pos, node_2.y_pos], 0)
		patch = generate_patch(translated_agent, facecolor="green", alpha=0.5)
		ax.add_patch(patch)

	if legend:
		plt.plot(-1, -1, color="r", label="Resolution Optimal Path")
		#plt.plot(-1, -1, color="g", label="Calculated Path")
		plt.scatter(x_array[path[0]], y_array[path[0]], color="goldenrod", 
		marker="s", s = 50, zorder=3, alpha=1.0, label="Start")

		plt.scatter(x_array[path[-1]], y_array[path[-1]], color="blueviolet",
		marker="s", s = 50, zorder=3, alpha=1.0, label="Goal")

		plt.legend(loc="upper left")

	return 