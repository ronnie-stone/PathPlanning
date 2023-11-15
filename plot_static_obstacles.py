import matplotlib.pyplot as plt
from generate_patch import generate_patch


def plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax):
	"""
	Plots user-defined obstacles in the specified axis.

		Parameters:

		static_obstacles (list of lists): Shape of static obstacles [X[0], Y[0], DX, DY].
		ax (matplotlib object): Axis to be plotted on.

		Returns:

			None

	"""

	plt.sca(ax)
	
	color = "blue"
	alpha = 0.8

	for obstacle in static_obstacles:
		patch = generate_patch(obstacle, facecolor=color, lw=1, alpha=alpha)
		ax.add_patch(patch)

	color = "red"
	alpha = 0.2

	for obstacle in dilated_static_obstacles:
		patch = generate_patch(obstacle, facecolor=color, lw=1, alpha=alpha)
		ax.add_patch(patch)

	ax.set_aspect(1)
	plt.tick_params(left=False,bottom=False)
	plt.xticks(color='w')
	plt.yticks(color='w')
	plt.axis([0, 10, 0, 10])

	return