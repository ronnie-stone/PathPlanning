import numpy as np
from node import Node 
from scipy.stats import norm
from scipy.optimize import minimize

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

	successors = []
	t = min_node.gcost
	current_interval = min_node.safe_intervals

	# M(S) to find neighboring configurations and c(s, s') = weight:

	for child_node_index, weight in min_node.edges.items():

		child_node = nodes[child_node_index]
		interval = child_node.safe_intervals

		mu_i = min_node.mean
		var_i = min_node.var
		a1 = current_interval[0]
		b1 = current_interval[1]

		mu_ij = weight
		var_ij = 0.001
		a2 = interval[0]
		b2 = interval[1]

		if a1 == 0 and b1 == float("Inf"):
			tw_1 = [0, float("Inf")]
		elif a1 != 0 and b1 == float("Inf"):
			constraints1 = {"type": "ineq", "fun": constraint_N1, "args": (mu_i, var_i, a1, b1, P_threshold)}
			results1 = minimize(lambda tw: tw, 0, constraints=constraints1, bounds=[(0, b1)])
			if not results1.success:
				continue
			else:

		else:
			constraints1 = {"type": "ineq", "fun": constraint_N1, "args": (mu_i, var_i, a1, b1, P_threshold)}
			results1 = minimize(lambda tw: tw, 0, constraints=constraints1, bounds=[(0, b1)])
			if not results1.success:
				continue
			results2 = minimize(lambda tw: -tw, results1.x[0], constraints=constraints1, bounds=[(results1.x[0], b1)])
			else:
				tw1
				print(results1.x[0])

		results2 = minimize(lambda )


		print(results1.x[0])
		 
		constraints = [{"type": "ineq", "fun": constraint_N1, "args": (mu_i, var_i, a1, b1, P_threshold)},
				       {"type": "ineq", "fun": constraint_N2, "args": (mu_i, mu_ij, var_i, var_ij, a2, b2, P_threshold)}]
		
		initial_guess = 0
		bounds = [(0, b1)]
		
		result = minimize(objective, initial_guess, constraints=constraints, bounds=bounds)
		success = result.success
		tw_optimal = result.x[0] if success else None
		
		if tw_optimal is None:
			continue

		if tw_optimal != 0:
			print(tw_optimal) 

		new_mean = mu_i + mu_ij + tw_optimal
		new_var = var_i + var_ij

		successors.append((child_node, (new_mean, new_var), new_mean))

	return successors

if __name__ == "__main__":
	pass