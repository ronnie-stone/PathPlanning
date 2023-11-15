class Node():

    def __init__(self, x_pos, y_pos, index):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.index = index
        self.gcost = float("Inf")
        self.hcost = float("Inf")
        self.fcost = float("Inf")
        self.visited = False
        self.open_interval = False
        self.predecessor = -1
        self.safe_intervals = []
        self.interval = []
        self.edges = dict()
        self.time = 0
        self.old = -1
        self.std = 0
        self.mean = 0

    def update_fcost(self):
        self.fcost = self.gcost + self.hcost

    def update_fcost_convolution(self):
        pass


    def find_current_interval(self, t):
        for interval in self.safe_intervals:
            if interval[0] <= t <= interval[1]:
                return interval
        else:
            print("You are currently in an invalid state")
            return [0, float("Inf")]

    def __lt__(self, other):
        if self.fcost < other.fcost:
            return True
        else:
            return False


    def add_connection(self, neighbor_index, distance_to_neighbor):
        self.connectivity_array[neighbor_index] = distance_to_neighbor

