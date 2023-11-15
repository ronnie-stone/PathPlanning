import numpy as np
import matplotlib.pyplot as plt
from fetch_agent import fetch_agent
from plot_static_obstacles import plot_static_obstacles

def rigid_body_motion(agent, displacement, theta):

	n_points_polygon = len(agent)
	translated_agent = np.zeros([n_points_polygon, 2])

	if theta == 0:

		for i in range(n_points_polygon):

			translated_agent[i,0] = agent[i,0] + displacement[0]
			translated_agent[i,1] = agent[i,1] + displacement[1]

	else:

		r_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])

		for i in range(n_points_polygon):

			translated_agent[i,:] = np.matmul(r_matrix, agent[i,:]) + displacement

	return translated_agent

if __name__ == "__main__":

	agent_original = fetch_agent("UnitOctagon")
	agent_translated = rigid_body_motion(agent_original, [7, 5], np.pi/8)

	fig1, ax1 = plt.subplots(1,1)
	plot_obstacles([agent_translated, agent_original], [], ax1)
	plt.show()