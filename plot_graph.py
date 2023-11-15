import matplotlib.pyplot as plt


def plot_graph(graph, ax):
	"""
	Plots the nodes and edges of any generated graph.

		Parameters:

		graph (Graph object): See class definition for information.
		ax (Matplotlib object): Axis to be plotted on.

		Returns:

			None

	"""

	plt.sca(ax)
	nodes = graph.nodes
	N = len(nodes)

	# Here we use a trick to speed up the plotting of multiple line segments.

	x = []
	y = []
	x_point = []
	y_point = []

	for i in range(N):
		node = nodes[i]
		edges = node.edges
		x_point.append(node.x_pos)
		x_point.append(None)
		y_point.append(node.y_pos)
		y_point.append(None)
		for edge in edges:
			neighbor_node = nodes[edge]
			x.append(node.x_pos)
			x.append(neighbor_node.x_pos)
			x.append(None)
			y.append(node.y_pos)
			y.append(neighbor_node.y_pos)
			y.append(None)

	plt.plot(x_point, y_point, 'ro', alpha=1.0, markersize=3, zorder=2, mec="black")
	plt.plot(x,y,color="k", alpha=0.5, zorder=1, lw=0.5)

	return