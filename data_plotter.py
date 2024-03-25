import os, glob 
from matplotlib.path import Path
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from data_algorithms import find_current_pose, find_current_pose_2, rigid_body_motion


def generate_patch(obstacle, facecolor="blue", lw=1, alpha=0.8):
    n_points_polygon = len(obstacle)-1
    move_sequence = [Path.MOVETO]
    for i in range(n_points_polygon-1):
        move_sequence.append(Path.LINETO)
    move_sequence.append(Path.CLOSEPOLY)
    patch_path = Path(obstacle, move_sequence)
    patch = patches.PathPatch(patch_path, facecolor=facecolor, lw=lw, alpha=alpha, zorder=0)
    return patch

def plot_object(object, ax, color="blue"):
    plt.sca(ax)
    patch = generate_patch(object, facecolor=color, alpha=1.0)
    ax.add_patch(patch)

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
    for obstacle in static_obstacles:
        patch = generate_patch(obstacle, facecolor="blue", lw=1, alpha=0.8)
        ax.add_patch(patch)
    for obstacle in dilated_static_obstacles:
        patch = generate_patch(obstacle, facecolor="red", lw=1, alpha=0.2)
        ax.add_patch(patch)

    ax.set_aspect(1)
    plt.tick_params(left=False,bottom=False)
    plt.xticks(color='w')
    plt.yticks(color='w')
    plt.axis([0, 10, 0, 10])

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

    x, y, x_point, y_point = [], [], [], []

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

def plot_path(graph, path, ax, legend=False, agent=[], t_array=[]):
    """
    Plots the path generated.

        Parameters:

        graph (Graph object): See class definition for information.
        path (N x 1 float array): Node indices that make up the path found.
        ax (Matplotlib object): Axis to be plotted on.

        Returns:

        None

    """

    # If path is empty, do not plot anything:

    if not path:
        return 

    plt.sca(ax)
    nodes = graph.nodes
    path_length = len(path)

    poses=False
    if len(agent) > 0:
        poses = True

    orientation = False
    if len(t_array) > 0:
        orientation = True

    for i in range(path_length - 1):

        node_1 = nodes[path[i]]
        node_2 = nodes[path[i+1]]
        plt.plot([node_1.x_pos, node_2.x_pos], [node_1.y_pos, node_2.y_pos],
        color="red", alpha=1.0, zorder=3, lw=1.0)

        if poses:
            if orientation:
                translated_agent = rigid_body_motion(agent, [node_1.x_pos, node_1.y_pos], t_array[k2])
            else:
                translated_agent = rigid_body_motion(agent, [node_1.x_pos, node_1.y_pos], 0)
            patch = generate_patch(translated_agent, facecolor="green", alpha=0.5)
            ax.add_patch(patch)

    if poses:
        translated_agent = rigid_body_motion(agent, [node_2.x_pos, node_2.y_pos], 0)
        patch = generate_patch(translated_agent, facecolor="green", alpha=0.5)
        ax.add_patch(patch)

    if legend:
        plt.plot(-1, -1, color="r", label="Resolution Optimal Path")
        #plt.plot(-1, -1, color="g", label="Calculated Path")
        plt.scatter(x_array[path[0]], y_array[path[0]], color="goldenrod", 
        marker="s", s = 50, zorder=3, alpha=1.0, label="Start")

        plt.scatter(x_array[path[-1]], y_array[path[-1]], color="blueviolet",
        marker="s", s = 50, zorder=3, alpha=1.0, label="Goal")

        plt.legend(loc="upper left")

    return 

def plot_safe_intervals(graph, t, ax):
    
    plt.sca(ax)
    x_red, y_red, x_green, y_green = [], [], [], []
    
    for node in graph.nodes:
        safe = False
        for interval in node.safe_intervals:
            if interval[0] <= t <= interval[1]:
                x_green.append(node.x_pos)
                x_green.append(None)
                y_green.append(node.y_pos)
                y_green.append(None)
                safe = True
                break
        if not safe:
            x_red.append(node.x_pos)
            x_red.append(None)
            y_red.append(node.y_pos)
            y_red.append(None)
    
    plt.plot(x_green, y_green, color="green", marker="o", mec="black")
    plt.plot(x_red, y_red, color="red", marker="o", mec="black")

def make_video(path, savename):

    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    frames = []
    for filename in sorted(glob.glob(CURR_DIR + path), key=os.path.getmtime):
        new_frame = Image.open(filename)
        frames.append(new_frame)
    frames[0].save(savename + ".gif", format="GIF", append_images=frames[1:], save_all=True, loop=0)

def simulate_intervals(graph, static_obstacles, dilated_static_obstacles, dynamic_obstacles, image_path, ax):
    end = 99
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    for filename in glob.glob(CURR_DIR + "/" + image_path + "/*.png"):
        os.remove(filename)
    i = 0
    while i < end:

        plt.sca(ax)
        plt.cla()

        # Image manipulation goes here.

        new_agent = dynamic_obstacles["pos"][i]
        plot_graph(graph, ax)
        plot_object(new_agent, ax)
        plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax)
        plot_safe_intervals(graph, i*0.1, ax)

        # Image manipulation ends. 
        step = '{:03d}'.format(i)
        plt.savefig(image_path + "/Step" + step)
        i += 1
    make_video("/" + image_path + "/*.png", "DEBUG")


def simulate_motion(graph, agent, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path, image_path, ax):
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    for filename in glob.glob(CURR_DIR + "/" + image_path + "/*.png"):
        os.remove(filename)
    dt = 0.1
    i = 0
    t = 0
    while t < graph.nodes[path[-1]].gcost - dt:

        plt.sca(ax)
        plt.cla()

        # Image manipulation goes here.

        p, theta = find_current_pose_2(graph, path, t)
        new_agent = rigid_body_motion(agent, p, theta)
        new_obs = dynamic_obstacles["pos"][i]
        #plot_graph(graph, ax)
        circ = plt.Circle((5,4.5), radius=1, color='g', fill=False)
        ax.add_patch(circ)
        plt.arrow(5,3.5,0.01,0,width=0.03, color='g')
        plot_path(graph, path, ax)
        print("Time: " + str(t) + "Step: " + str(i))
        plot_object(new_agent, ax, color="blue")
        plot_object(new_obs, ax, color="green")
        plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax)

        # Image manipulation ends. 
        step = '{:03d}'.format(i)
        plt.savefig(image_path + "/Step" + step)
        i += 1
        t += dt
    make_video("/" + image_path + "/*.png", "DEBUG")

def simulate_motion_multi(graph1, graph2, agent1, agent2, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path1, path2, image_path, ax):
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    for filename in glob.glob(CURR_DIR + "/" + image_path + "/*.png"):
        os.remove(filename)
    dt = 0.1
    i = 0
    t = 0
    while t < 20 - dt:

        plt.sca(ax)
        plt.cla()

        # Image manipulation goes here.

        p1, theta1 = find_current_pose_2(graph1, path1, t)
        p2, theta2 = find_current_pose_2(graph2, path2, t)
        new_agent1 = rigid_body_motion(agent1, p1, theta1)
        new_agent2 = rigid_body_motion(agent2, p2, theta2)
        new_obs = dynamic_obstacles["pos"][i]
        #plot_graph(graph, ax)
        #circ = plt.Circle((5,4.5), radius=1, color='g', fill=False)
        #ax.add_patch(circ)
        #plt.arrow(5,3.5,0.01,0,width=0.03, color='g')
        plot_path(graph1, path1, ax)
        plot_path(graph2, path2, ax)
        print("Time: " + str(t) + "Step: " + str(i))
        plot_object(new_agent1, ax, color="blue")
        plot_object(new_agent2, ax, color="blue")
        plot_object(new_obs, ax)
        plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax)

        # Image manipulation ends. 
        step = '{:03d}'.format(i)
        plt.savefig(image_path + "/Step" + step)
        i += 1
        t += dt
    make_video("/" + image_path + "/*.png", "DEBUG")