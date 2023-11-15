class State():

    def __init__(self, index, safe_interval, time):
        self.index = index
        self.safe_interval = safe_interval
        self.time = 0
        self.visited = False
        self.predecessor = -1

    def update_fcost(self):
        self.fcost = self.gcost + self.hcost

    def find_current_interval(self):
        return safe_interval

    def __lt__(self, other):
        if self.fcost < other.fcost:
            return True
        else:
            return False