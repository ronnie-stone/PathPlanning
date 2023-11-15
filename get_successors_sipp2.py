import numpy as np
from node import Node 


def get_successors_sipp2(min_node, nodes):

	successors = []
	t = min_node.gcost
	current_interval = min_node.safe_intervals

	if current_interval[0] > t or current_interval[1] < t:
		print(t, current_interval)
		
	# M(S) to find neighboring configurations and c(s, s') = weight:

	for child_node_index, weight in min_node.edges.items():

		child_node = nodes[child_node_index]
		interval = child_node.safe_intervals
		start_t = t + weight
		end_t = current_interval[1] + weight
		if interval[0] > end_t or interval[1] < start_t:
			continue
		new_t = max(start_t, interval[0])
		successors.append((child_node, weight, new_t))

	return successors


if __name__ == "__main__":

	# Define node SB as in the paper:

    node_SB0 = Node(5,5,0)
    node_SB0.safe_intervals = [0,4]

    node_SB1 = Node(5,5,1)
    node_SB1.safe_intervals = [6,float("Inf")]

    node_SA0 = Node(5,6,2)
    node_SA0.safe_intervals = [0,5]

    node_SA1 = Node(5,6,3)
    node_SA1.safe_intervals = [7, float("Inf")]

    node_SC0 = Node(5,4,4)
    node_SC0.safe_intervals = [0, 1]

    node_SC1 = Node(5,4,5)
    node_SC1.safe_intervals = [3, 3]

    node_SC2 = Node(5,4,6)
    node_SC2.safe_intervals = [5, float("Inf")]
    
    node_SB0.edges[2] = 1
    node_SB0.edges[3] = 1
    node_SB0.edges[4] = 1
    node_SB0.edges[5] = 1
    node_SB0.edges[6] = 1
    node_SB0.gcost = 0
    nodes = [node_SB0, node_SB1, node_SA0, node_SA1, node_SC0, node_SC1, node_SC2]
    sucessors = get_successors_sipp2(node_SB0, nodes)

    for node, weight, time in sucessors:
	    print(node.index, weight, time)