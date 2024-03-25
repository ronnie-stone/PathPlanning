import numpy as np
import heapq as hp
from get_successors_sipp3 import get_successors_sipp3

def sipp3(graph):

	def heuristic(node_index_1, node_index_2):

		node_1 = graph.nodes[node_index_1]
		node_2 = graph.nodes[node_index_2]

		h = np.sqrt((node_1.x_pos - node_2.x_pos)**2 + (node_1.y_pos - node_2.y_pos)**2)

		return h

	# First we fetch the vector of nodes:

	nodes = graph.nodes
	N = len(nodes)
	start_index = N - 2
	end_index = N - 1

	# Define what the initial node is:

	min_node = nodes[start_index]
	min_node.gcost = 0
	min_node.hcost = heuristic(start_index, end_index)
	min_node.update_fcost()

	# Create a priority queue to deal with search progression:

	pqueue = []
	hp.heappush(pqueue, min_node)

	# While there are nodes to be explored:

	while pqueue:

		min_node = hp.heappop(pqueue)
		min_node.visited = True
		successors = get_successors_sipp3(min_node, graph.nodes, 0.95)

		for child_node, weight, time in successors:

			if child_node.gcost > time:
				child_node.gcost = time
				child_node.hcost = heuristic(child_node.index, end_index)
				child_node.update_fcost()
				child_node.mean = weight[0]
				child_node.var = weight[1]
				child_node.predecessor = min_node.index
				hp.heappush(pqueue, nodes[child_node.index])

		if min_node.index == end_index:
			break

	# Reconstructing the path:

	if nodes[end_index].predecessor == -1:
		print("Unreacheable Path")
		return [], float("Inf")

	path = []
	total_cost = 0
	currentNode = end_index

	while currentNode != start_index:
		node = nodes[currentNode]
		path.append(node.predecessor)
		total_cost += node.edges[node.predecessor]
		currentNode = node.predecessor

	path.reverse()
	path.append(end_index)

	print(total_cost)
	return path, graph.nodes[path[-1]].gcost