import numpy as np
from graph import Graph
from data_algorithms import generate_trajectory


def read_line(line, offset=0):
    vertices = []
    raw_data = line.strip().split(" ")
    for i in range(len(raw_data)-offset):
        coords = raw_data[i][1:-1].split(",")
        vertices.append([float(coords[0]), float(coords[1])])
    return vertices

def fetch_agent(path):
    with open("Agents/" + path + ".txt", "r") as f:
        for line in f:
            vertices = read_line(line)
    return np.asarray(vertices, dtype=float)
    
def fetch_static_obstacles(path):
    static_obstacles = []
    with open("StaticObstacles/" + path + ".txt", "r") as f:
        for line in f:
            vertices = read_line(line)
            translation = vertices[-1]
            for i in range(len(vertices)-1):
                vertices[i][0] += translation[0]
                vertices[i][1] += translation[1]
            static_obstacles.append(vertices[:-1])
    return static_obstacles
    
def fetch_dynamic_obstacles(agent_path, traj_path):
    dynamic_obstacles = dict()
    initial_shape = fetch_agent(agent_path)
    dynamic_obstacles["shape"] = initial_shape
    dynamic_obstacles["pos"] = []
    generate_trajectory(initial_shape, (4,4.5), (6,4.5), constant=True)
    with open("Trajectories/" + traj_path + ".txt", "r") as f:
        for line in f:
            dynamic_obstacles["pos"].append(read_line(line, offset=1))
    dynamic_obstacles["pos"] = np.asarray(dynamic_obstacles["pos"], dtype=float)
    return dynamic_obstacles
