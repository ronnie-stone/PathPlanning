import numpy as np
from node import Node 


def get_successors_sipp(min_node, t, nodes):

	successors = []

	# M(S) to find neighboring configurations and c(s, s') = weight:

	for child_node_index, weight in min_node.edges.items():

		child_node = nodes[child_node_index]
		current_interval = min_node.find_current_interval(t)

		start_t = t + weight
		end_t = current_interval[1] + weight

		# At this point we are at the state level:

		for i in range(len(child_node.safe_intervals)):

			interval = child_node.safe_intervals[i]
			if interval[0] > end_t or current_interval[1] < start_t:
				continue

			# Need to somehow do the collision checking here.
			# But I think we can possibly ignore this. 

			# If start_t is chosen, this means there is no wait. 
			# If interval[0] is chose, that we wait until the dynamic obstacle passes.

			new_t = max(start_t, interval[0])
			successors.append((child_node, i, new_t))

	return successors


if __name__ == "__main__":

	# Define node SB as in the paper:

	node_B = Node(5, 5, 0)
	node_B.safe_intervals = [[0, 4], [5, float("Inf")]]
	node_B.edges[1] = 1
	node_B.edges[2] = 1
	node_B.gcost = 0

	# Define node SA as in the paper:

	node_A = Node(6, 5, 1)
	node_A.safe_intervals = [[0,5], [7, float("Inf")]]

	# Define node SC as in the paper:

	node_C = Node(4, 5, 2)
	node_C.safe_intervals = [[0,1], [3,3], [5, float("Inf")]]

	nodes = [node_B, node_A, node_C]

	sucessors = get_successors_sipp(node_B, 0, nodes)

	for node, interval_index, time in sucessors:
		print(node.index, node.safe_intervals[interval_index], time)

