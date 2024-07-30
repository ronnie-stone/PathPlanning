import numpy as np
from node import Node 
from scipy.stats import norm
from scipy.optimize import minimize
from find_min_phi_for_N2 import find_min_phi_for_N2
import time

def check_shifted_distribution(mu, var, a2, b2, P_threshold, running_prob):
	cdf_a2 = norm.cdf(a2, mu, var**0.5)
	cdf_b2 = norm.cdf(b2, mu, var**0.5)
	area = cdf_b2 - cdf_a2
	is_satisfied = (area*running_prob >= P_threshold)
	return is_satisfied, area

def get_successors_sipp3(min_node, nodes, P_threshold):

	# Initialize list of successors. Current interval is bounds of safe interval of min node.

	successors = []
	current_interval = min_node.safe_intervals

	# Iterate over nodes connected to min node.

	for child_node_index, weight in min_node.edges.items():

		# Fetch current child node and its safe interval bounds. If it is tagged as visited, ignore. 

		child_node = nodes[child_node_index]
		child_interval = child_node.safe_intervals
		if child_node.visited: continue

		# Min node has a cumulative mean and variance. 

		mu_i = min_node.mean
		var_i = min_node.var
		running_prob = min_node.running_prob

		a1 = current_interval[0]
		b1 = current_interval[1]

		# The edge to child node has a mean equal to its weight and an associated variance.

		mu_ij = weight

		# For fixed uncertainty:
		var_ij = 0.005
  
		# For space-varying uncertainty (diagonal split):
		#if child_node.y_pos <= (-child_node.x_pos + 10):
		#	var_ij = 0.05
		#else:
		#	var_ij = 0.08

		a2 = child_interval[0]
		b2 = child_interval[1]

		# If dynamic obstacle never crosses child node, i.e. sf = [0, inf], optimal waiting time is zero:

		if a2 == 0 and b2 == float("inf"):
			successors.append((child_node, (mu_i + mu_ij, var_i + var_ij, 1.0), mu_i + mu_ij))
			continue

		# Check if zero waiting time works. If not, and b2 is smaller or equal to the shifted mean, then there is no solution. 

		is_satisfied, area = check_shifted_distribution((mu_i + mu_ij), (var_i + var_ij), a2, b2, P_threshold, running_prob)
		if is_satisfied:
			successors.append((child_node, (mu_i + mu_ij, var_i + var_ij, area), mu_i + mu_ij))
			continue
		else: 
			if b2 <= (mu_i + mu_ij):
				continue

		# Now we look for the lower bound for N2 constraint and check if it satisfies N1 constraint:

		tw_2_lb = find_min_phi_for_N2(mu_i, var_i, mu_ij, var_ij, a2, b2, P_threshold*running_prob)
		if tw_2_lb == (-1):
			continue
		else:
			is_satisfied, area = check_shifted_distribution((mu_i + tw_2_lb), (var_i), a1, b1, P_threshold, running_prob)
			if is_satisfied: 
				successors.append((child_node, (mu_i + mu_ij + tw_2_lb, var_i + var_ij, area), mu_i + mu_ij + tw_2_lb))
				continue
			else: continue

	return successors

if __name__ == "__main__":
	pass