import numpy as np 
import random as rd
from data_algorithms import generate_bounding_box, is_valid_pose_shapely, rigid_body_motion
from node3D import Node3D
from graph_3D import Graph3D
from scipy.spatial import KDTree


def prm_3D(obstacles, agent, N=1000, xlim=(0, 10), ylim=(0, 10), k=6):
	"""
	Implementation of PRM using custom classes. 

		Parameters:

			obstacles (list of lists): Shape of obstacles.
			agent (list of tuples): Shape of agent.
			N (int): Number of samples.
			xlim (float 2-tuple): Enviroment x bounds.
			ylim (float 2-tuple): Enviroment y bounds.
			k (int): Approximate number of neighbors for each node.

		Returns:

			edges (int-list dictionary): Nodes' IDs and connectivities.
			x_array (N x 1 float array): Nodes' x coordinates.
			y_array (N x 1 float array): Nodes' y coordinates.

	"""

	# Define data structures:

	agent_bb = generate_bounding_box(agent)
	x_buffer = (agent_bb[2][0] - agent_bb[0][0])/2
	y_buffer = (agent_bb[2][1] - agent_bb[0][0])/2
	point_array = np.zeros([N,3])
	graph = Graph3D()

	i = 0

	while i < N:

		# Sample random point in configuration space:

		x = rd.uniform(xlim[0]+x_buffer, xlim[1]-x_buffer)
		y = rd.uniform(ylim[0]+y_buffer, ylim[1]-y_buffer)
		theta = rd.uniform(0, 2*np.pi)
		p = (x,y)
		translated_agent = rigid_body_motion(agent, p, theta)

		# Check if point is valid:

		if is_valid_pose_shapely(obstacles, translated_agent):

			# Create node: 

			node = Node3D(x, y, theta, i)
			graph.add_node(node)
			point_array[i] = np.asarray([x, y, theta])
			i += 1

	# We build a KDTree to speed up k-neighbor calculations:

	tree = KDTree(point_array)

	for i in range(N):
		dist, ind = tree.query([point_array[i]], k=k+1)
		distances = dist[0]
		indices = ind[0]

		for j in range(1,k+1):
			graph.nodes[i].edges[indices[j]] = distances[j]

	graph.add_kdtree(tree)
	graph.enforce_symmetry()

	return graph