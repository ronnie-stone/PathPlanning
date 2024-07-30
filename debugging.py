import matplotlib.pyplot as plt
import numpy as np
import os, glob, time, json
from prm import prm
from prm_3D import prm_3D
from graph_3D import Graph3D
from graph import Graph
from scipy.stats import norm
from data_fetcher import fetch_agent, fetch_static_obstacles, fetch_dynamic_obstacles
import data_algorithms as da
import data_plotter as dp
from sipp2 import sipp2
from sipp3 import sipp3

def check_shifted_distribution(mu, var, a2, b2, P_threshold):
    cdf_a2 = norm.cdf(a2, mu, var**0.5)
    cdf_b2 = norm.cdf(b2, mu, var**0.5)
    area = cdf_b2 - cdf_a2
    is_satisfied = (area >= P_threshold)
    return is_satisfied, area

agent = fetch_agent("UnitOctagon")/2
static_obstacles = fetch_static_obstacles("PolygonsSIPP")
dynamic_obstacles = fetch_dynamic_obstacles("LongRectangle", "Circular")
dilated_static_obstacles = da.dilate_obstacles(static_obstacles, res=2)

# Graph name:

filename = "./Graph/graph_1000_10_FINAL"

# Graph creation:

#graph = prm(dilated_static_obstacles, agent, N=5000, k=10)
#graph.add_query_points((8, 1.5), (1.5, 8))
#da.calculate_safe_intervals(graph, dynamic_obstacles, agent)
#graph.generate_new_nodes()
#graph.save_graph(filename)

# Fetching graph:

with open(filename, "r") as f:
    data = json.loads(f.read())
    graph = Graph.deserialize(data)

fig1, ax1 = plt.subplots(1,1)
fig1.set_size_inches(10,10)
#dp.plot_graph(graph, ax1)
#dp.plot_static_obstacles(static_obstacles, dilated_static_obstacles, ax1, facecolor="black", buffercolor="white")
#plt.show()



#pbounds = [0.5]
#color_scheme = ["red"]
pbounds = [0, 0.5, 0.6, 0.7, 0.8, 0.9999]
plans = []
color_scheme = ["red", "blue", "gold", "magenta", "green", "cyan"]
i = 0
for pbound in pbounds:
    path, total_cost = sipp3(graph, pbound)
    plan = da.path_to_plan(path, graph)
    plans.append(plan)
    dp.plot_path(graph, path, ax1, color=color_scheme[i])
    graph = Graph.deserialize(data)
    i += 1
circ = plt.Circle((5,4.5), radius=1, color='k', fill=False)
ax1.add_patch(circ)
plt.arrow(5,3.5,0.01,0,width=0.03, color='k')
start_agent = da.rigid_body_motion(agent, (1.5,8), 0)
final_agent = da.rigid_body_motion(agent, (8, 1.5), 0)
dp.plot_object(start_agent, ax1, color="black", alpha=0.5)
dp.plot_object(final_agent, ax1, color="black", alpha=0.5)
dp.plot_object(dynamic_obstacles["pos"][0], ax1, color="black", alpha=0.5)


"""


pbound = 0.99
path, total_cost = sipp3(graph, pbound)
dp.plot_path(graph, path, ax1, color="red")
circ = plt.Circle((5,4.5), radius=1, color='k', fill=False)
ax1.add_patch(circ)
plt.arrow(5,3.5,0.01,0,width=0.03, color='k')
start_agent = da.rigid_body_motion(agent, (1.5,8), 0)
final_agent = da.rigid_body_motion(agent, (8, 1.5), 0)
dp.plot_object(start_agent, ax1, color="black", alpha=0.5)
dp.plot_object(final_agent, ax1, color="black", alpha=0.5)
dp.plot_object(dynamic_obstacles["pos"][0], ax1, color="black", alpha=0.5)
plan = da.path_to_plan(path, graph)

"""

def monte_carlo(plan):

    expected_running_cost = 0
    running_cost = 0 
    running_var = 0
    nodes = graph.nodes

    for action in plan:

        tol = 1e-3
        if action[0] == "T":
            action_type, ni, nj, action_cost = action

            # Need to find the edge function:

            var_f = 0.005
            time = np.random.normal(action_cost, np.sqrt(var_f), 1)
            safe_intervals = nodes[nj].safe_intervals

            #print("T", action_cost, mu_f, time)

            expected_running_cost += action_cost
            running_cost += np.mean(time)
            running_var += var_f

            is_satisfied, _ = check_shifted_distribution(expected_running_cost, running_var, safe_intervals[0], safe_intervals[1], pbound)

            if not is_satisfied: pass
                #print("here")

            if running_cost <= 0:
                continue

            if running_cost < safe_intervals[0] or running_cost > safe_intervals[1]:
                #print(running_cost)
                #print(nodes[nj].safe_intervals)
                #print()
                return False, running_cost

        else:
            action_type, ni, action_cost = action
            running_cost += action_cost
            print(running_cost)

            if running_cost <= 0: continue

            if running_cost < nodes[ni].safe_intervals[0] or running_cost > nodes[ni].safe_intervals[1]:
                print(running_cost, nodes[ni].safe_intervals)
                return False, running_cost

    return True, running_cost

success_ratio = []
for plan in plans:
    n_success = 0
    for i in range(1000):
        success, running_cost = monte_carlo(plan)
        if success:
            n_success += 1
    success_ratio.append(n_success)

print(success_ratio)
plt.show()


#dp.simulate_motion(graph, agent, static_obstacles, dilated_static_obstacles, dynamic_obstacles, path, "Images", ax1)
