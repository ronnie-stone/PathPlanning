import numpy as np
from node import Node 
from scipy.stats import norm
from scipy.optimize import minimize
from find_min_phi_for_N2 import find_min_phi_for_N2
import time


def custom_optimization(mu_i, var_i, mu_ij, var_ij, a1, b1, a2, b2, P_threshold, successors, child_node):

	# Try custom bounds search:
		delta_tw = 0.01
		t_values = np.linspace(delta_tw, 1, num=100)
			
		for tw in t_values:
			is_satisfied_N1, area_N1 = check_shifted_distribution(mu_i, var_i, a1, b1, P_threshold, tw)
			is_satisfied_N2, area_N2 = check_shifted_distribution((mu_i + mu_ij), (var_i + var_ij), a2, b2, P_threshold, tw)

			if not is_satisfied_N1: 
				break 

			if is_satisfied_N2:
				new_mean = mu_i + mu_ij + tw
				new_var = var_i + var_ij
				successors.append((child_node, (new_mean, new_var), new_mean))
				break

def check_shifted_distribution(mu, var, a2, b2, P_threshold, t):
	cdf_a2 = norm.cdf(a2, mu+t, var**0.5)
	cdf_b2 = norm.cdf(b2, mu+t, var**0.5)
	area = cdf_b2 - cdf_a2
	is_satisfied = (area >= P_threshold)
	return is_satisfied, area

def constraint_N1(tw, mu_i, var_i, a1, b1, P_threshold):
	mean = mu_i + tw
	std_dev = var_i ** 0.5
	return norm.cdf(b1, mean, std_dev) - norm.cdf(a1, mean, std_dev) - P_threshold

def constraint_N2(tw, mu_i, mu_ij, var_i, var_ij, a2, b2, P_threshold):
    mean = mu_i + mu_ij + tw
    std_dev = (var_i + var_ij) ** 0.5
    return norm.cdf(b2, mean, std_dev) - norm.cdf(a2, mean, std_dev) - P_threshold

def objective(tw):
	return tw

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
		a1 = current_interval[0]
		b1 = current_interval[1]

		# The edge to child node has a mean equal to its weight and an associated variance.

		mu_ij = weight
		var_ij = 0.01
		a2 = child_interval[0]
		b2 = child_interval[1]

		# If dynamic obstacle never crosses child node, i.e. sf = [0, inf], optimal waiting time is zero:

		if a2 == 0 and b2 == float("inf"):
			successors.append((child_node, (mu_i + mu_ij, var_i + var_ij), mu_i + mu_ij))
			continue

		# Check if zero waiting time works. If not, and b2 is smaller or equal to the shifted mean, then there is no solution. 

		is_satisfied, _ = check_shifted_distribution((mu_i + mu_ij), (var_i + var_ij), a2, b2, P_threshold, 0)
		if is_satisfied:
			successors.append((child_node, (mu_i + mu_ij, var_i + var_ij), mu_i + mu_ij))
			continue
		else: 
			if b2 <= (mu_i + mu_ij): continue

		# Now we look for the lower bound for N2 constraint and check if it satisfies N1 constraint:

		tw_2_lb = find_min_phi_for_N2(mu_i, var_i, mu_ij, var_ij, a2, b2, P_threshold*100)
		if tw_2_lb == (-1):
			continue
		else:
			is_satisfied, _ = check_shifted_distribution((mu_i + tw_2_lb), (var_i), a1, b1, P_threshold,  0)
			if is_satisfied: 
				successors.append((child_node, (mu_i + mu_ij + tw_2_lb, var_i + var_ij), mu_i + mu_ij + tw_2_lb))
				continue
			else: continue

	return successors

if __name__ == "__main__":
	pass