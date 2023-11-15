import shapely as shp
import numpy as np


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

def dilate_obstacles(static_obstacles, eps=0.1, res=1):
    dilated_static_obstacles = []
    for obstacle in static_obstacles:
        polygon = shp.geometry.Polygon(obstacle)
        polygon_with_buffer = shp.buffer(polygon, eps, quad_segs=res)
        dilated_static_obstacles.append(list(polygon_with_buffer.exterior.coords))
    return dilated_static_obstacles

def generate_trajectory(agent, start, end, dt=0.1, speed=1.0, time=20.0, constant=False):
    if constant:
        Nt = int(time/dt)
        trajectory = np.zeros([Nt,2])
        t = 0 
        with open("Trajectories/Constant.txt", "w") as f:
            for i in range(Nt):
                for p in agent:
                    if p[0] < 0:
                        p[0] -= 0.019
                    if p[0] > 0:
                        p[0] += 0.019
                    if p[1] < 0:
                        p[1] -= 0.01
                    if p[1] > 0:
                        p[1] += 0.01
                translated_agent = rigid_body_motion(agent, (5,5), 0)
                for p in translated_agent:
                    f.write("(" + str(p[0]) + "," + str(p[1]) + ") ")
                f.write("(" + str(t) + ")\n")
                t += dt
    else:
        def circle(radius, midpoint, t):
            return (midpoint[0] + radius*np.cos(t), midpoint[1] + radius*np.sin(t))
        midpoint = ((start[0] + end[0])/2, (start[1] + end[1])/2)
        radius = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2)/2
        Nt = int(time/dt)
        trajectory = np.zeros([Nt, 2])
        t = 0 
        with open("Trajectories/Circular.txt", "w") as f:
            for i in range(Nt):
                theta = speed*t
                trajectory[i,:] = circle(radius, midpoint, theta)
                translated_agent = rigid_body_motion(agent, trajectory[i, :], 0)
                for p in translated_agent:
                    f.write("(" + str(p[0]) + "," + str(p[1]) + ") ")
                f.write("(" + str(t) + ")\n")
                t += dt

def generate_bounding_box(objects):
    sorted_x = np.argsort(objects[:,0])
    sorted_y = np.argsort(objects[:,1])
    xmin = objects[sorted_x,:][0][0]
    xmax = objects[sorted_x,:][-1][0]
    ymin = objects[sorted_y,:][0][1]
    ymax = objects[sorted_y,:][-1][1]
    agent_bb = np.array([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax], [xmin, ymin]])
    return agent_bb

def is_valid_pose_shapely(obstacles, agent): 
    agent_poly = shp.Polygon(agent)
    for obs in obstacles:
        if agent_poly.intersects(shp.Polygon(obs)):
            return False
    return True 

def calculate_safe_intervals(graph, dynamic_obstacle, agent, dt = 0.1):

    t = 0
    pos_dobs = dynamic_obstacle["pos"]
    #agent_bb = generate_bounding_box(agent)
    #x_buffer = (agent_bb[2][0] - agent_bb[0][0])/2
    #y_buffer = (agent_bb[2][1] - agent_bb[0][0])/2
    #diag_buffer = np.sqrt(x_buffer**2 + y_buffer**2)
    N = len(pos_dobs)

    for i in range(N):
        translated_dobs = pos_dobs[i]

        for node in graph.nodes:
            translated_agent = rigid_body_motion(agent, (node.x_pos, node.y_pos), 0)
            # translated_agent = rigid_body_motion(agent, (node.x_pos, node.y_pos), node.theta)

            # Consider using bounding box later.

            if is_valid_pose_shapely([translated_dobs], translated_agent):
                if not node.open_interval:
                    node.interval.append(t)
                    node.open_interval = True
            else:
                if node.open_interval:
                    node.interval.append(t)
                    node.open_interval = False
            if (len(node.interval)) == 2:
                node.safe_intervals.append(node.interval)
                node.interval = []
            if i == N-1:
                if len(node.interval) == 1:
                    node.interval.append(float("Inf"))
                    node.safe_intervals.append(node.interval)
        t += dt

def calculate_safe_intervals_multi(graph, dynamic_obstacle, agent, dt = 0.1):

    t = 0
    pos_dobs_1 = dynamic_obstacle[0]["pos"]
    pos_dobs_2 = dynamic_obstacle[1]["pos"]
    N = len(pos_dobs_1)

    for i in range(N):
        translated_dobs_1 = pos_dobs_1[i]
        translated_dobs_2 = pos_dobs_2[i]

        for node in graph.nodes:
            translated_agent = rigid_body_motion(agent, (node.x_pos, node.y_pos), 0)
            # translated_agent = rigid_body_motion(agent, (node.x_pos, node.y_pos), node.theta)

            # Consider using bounding box later.

            if is_valid_pose_shapely([translated_dobs_1], translated_agent) and is_valid_pose_shapely([translated_dobs_2], translated_agent):
                if not node.open_interval:
                    node.interval.append(t)
                    node.open_interval = True
            else:
                if node.open_interval:
                    node.interval.append(t)
                    node.open_interval = False
            if (len(node.interval)) == 2:
                node.safe_intervals.append(node.interval)
                node.interval = []
            if i == N-1:
                if len(node.interval) == 1:
                    node.interval.append(float("Inf"))
                    node.safe_intervals.append(node.interval)
        t += dt

def find_current_pose(graph, path, t):
    i = 0 
    cumulative_distance = 0
    while i < len(path) - 1:
        node_1 = graph.nodes[path[i]]
        node_2 = graph.nodes[path[i+1]]
        dist_1 = cumulative_distance
        dist_2 = dist_1 + node_1.edges[path[i+1]]
        if dist_1 <= t <= dist_2:
            dir_vec = np.array([node_2.x_pos - node_1.x_pos, node_2.y_pos - node_1.y_pos])
            unit_dir_vec = dir_vec/np.linalg.norm(dir_vec)
            offset = t - dist_1
            p = (node_1.x_pos + unit_dir_vec[0]*offset, node_1.y_pos + unit_dir_vec[1]*offset)
            return p, 0
        else:
            cumulative_distance = dist_2
        i += 1

def find_current_pose_2(graph, path, t):
    closest_dist = float("Inf")
    for i in range(len(path)):
        dist = abs(t-graph.nodes[path[i]].gcost)
        if dist < closest_dist:
            closest_dist = dist
            if i == 0:
                min_index = path[i]
            else:
                min_index = path[i-1]
    return (graph.nodes[min_index].x_pos, graph.nodes[min_index].y_pos), 0
    # return (graph.nodes[min_index].x_pos, graph.nodes[min_index].y_pos), graph.nodes[min_index].theta

