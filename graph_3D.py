import copy
import random as rd
from node3D import Node3D


class Graph3D():

    def __init__(self):
        self.nodes = []
        self.kdtree = None
        self.size = 0

    def add_node(self, node):
        self.nodes.append(node)
        self.size += 1

    def add_kdtree(self, kdtree):
        self.kdtree = kdtree

    def enforce_symmetry(self):
        for i in range(self.size):
            node_i_edges = self.nodes[i].edges
            for index in node_i_edges:
                node_neighbor_edges = self.nodes[index].edges
                if i not in node_neighbor_edges:
                   node_neighbor_edges[i] = node_i_edges[index]

    def generate_new_nodes(self):
        i = 0
        N = copy.deepcopy(self.size)
        while i < N:
            cur_node = self.nodes[i]
            for interval in cur_node.safe_intervals:
                new_node = Node3D(cur_node.x_pos, cur_node.y_pos, cur_node.theta, self.size-N)
                new_node.safe_intervals = interval
                new_node.edges = cur_node.edges
                new_node.old = i
                self.add_node(new_node)
            i += 1
        for j in range(N, self.size):
            cur_node = self.nodes[j]
            new_edges = dict()
            for index, weight in cur_node.edges.items():
                for k in range(N, self.size):
                    if k != j:
                        other_node = self.nodes[k]
                        if other_node.old == index:
                            new_edges[k-N] = weight
            cur_node.edges = new_edges
        self.nodes = self.nodes[N:]
        self.size = self.size-N

    def print_graph(self):
        for i in range(self.size):
            cur_node = self.nodes[i]
            print("Index: " + str(cur_node.index) + " X: " f'{cur_node.x_pos:.2f}' + " Y: " f'{cur_node.y_pos:.2f}' + " Old Index: " + str(cur_node.old))
            print("Safe Intervals: ")
            for interval in cur_node.safe_intervals:
                formatted_list = ['%.2f' % elem for elem in interval]
                print(formatted_list)
            print("Connectivity: ")
            print(cur_node.edges)
            print()

    def add_query_points(self, start_point, end_point):
        dist_1, index_1 = self.kdtree.query([start_point])
        dist_2, index_2 = self.kdtree.query([end_point])

        # Add start node:

        start_node = Node3D(start_point[0], start_point[1], start_point[2], self.size)
        self.add_node(start_node)
        start_node.edges = {index_1[0]:dist_1[0]}
        self.nodes[index_1[0]].edges[self.size-1] = dist_1[0]

        # Add end node:

        end_node = Node3D(end_point[0], end_point[1], end_point[2], self.size) 
        self.add_node(end_node)
        end_node.edges = {index_2[0]:dist_2[0]}
        self.nodes[index_2[0]].edges[self.size-1] = dist_2[0]

        return self.size-2, self.size-1

    def remove_query_points(self):
        for i in range(2):
            self.nodes.pop()