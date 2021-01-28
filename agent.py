from gridworld import Agent
import random
from collections import defaultdict

class MAFAgent(Agent):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.counter = 0
        self.prev_dx = 0  # TODO: depends on homebase location and first direction
        self.prev_dy = 0  # TODO: depends on homebase location and first direction
        self.pos_unexplored = []
        self.pos_explored = []
        self.return_mode = False

    def scan_for_target(self):
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (self.x + dx, self.y + dy) not in self.map:
                    if self.world.get_cell(self, dx, dy) == 'target':
                        return dx, dy
        return None, None

    def fill_cell_lists(self):
        self.pos_unexplored = []  # make sure to clear all list before obtaining dx and dy
        self.pos_explored = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if (self.x + dx, self.y + dy) in self.map:
                    self.pos_explored.append((dx, dy))
                elif self.world.get_cell(self, dx, dy) == 'empty':
                    self.pos_unexplored.append((dx, dy))

    def get_counter(self, at):
        dx, dy = at
        return self.map[self.x + dx, self.y + dy]


    def go_to_lowest_counter(self):
        return min(self.pos_explored, key=self.get_counter)

    def go_to_highest_counter(self):
        return max(self.pos_explored, key=self.get_counter)


    def go_to_unexplored(self, prob=95):
        if random.randint(0, 100) <= prob:
            return random.choice(self.pos_unexplored)
        if self.pos_explored:
            return self.go_to_explored()
        else:
            return random.choice(self.pos_unexplored)

    def go_to_explored(self, prob=95):
        highest = self.go_to_highest_counter()
        if random.randint(0, 100) <= prob or len(self.pos_explored) == 1:
            return highest
        return random.choice([pos for pos in self.pos_explored if pos != highest])

    def go_to_same_dir(self):
        if (random.randint(0, 100) <= 95 and (self.x + self.prev_dx, self.y + self.prev_dy) not in self.map and
           self.world.get_cell(self, self.prev_dx, self.prev_dy) == 'empty'):
            return self.prev_dx, self.prev_dy
        elif self.pos_unexplored:
            return self.go_to_unexplored()
        elif self.pos_explored:
            return self.go_to_explored()
        else:
            raise ValueError('Agent stuck -> no explored cells or unexplored cells.')

    def move(self):
        # sync map if agent finds other agent
        self.fill_cell_lists()
        if self.world.get_cell(self, 0, 0) == 'home':
            self.sync_map(self.world.home_base)
            self.return_mode = False
            self.counter = 0
        # agent goes to home base if it was in return mode in the previous agent-update
        if self.return_mode or self.world.get_cell(self, 0, 0) == 'target':
            self.return_mode = True
            dx, dy = self.go_to_lowest_counter()
        else:
            dx, dy = self.explore()
            self.counter += 1
            self.map[(self.x + dx, self.y + dy)] = self.counter
        self.prev_dx = dx
        self.prev_dy = dy
        return dx, dy

    def explore(self):
        dx, dy = self.scan_for_target()
        if dx is not None and dy is not None:
            if random.randint(0, 100) <= 95:
                return dx, dy
        return self.go_to_same_dir()

class IMAFAgent(MAFAgent):
    def __init__(self, *args):
        super().__init__(*args)
        self.last_communications = defaultdict(int)
    def move(self):
        for other_agent in self.world.get_nearby_agents(self):
            if self.last_communications[other_agent] >= 50:
                self.sync_map(other_agent)
                self.last_communications[other_agent] = 0
                other_agent.last_communications[self] = 0
        for key in list(self.last_communications):
            self.last_communications[key] += 1
        return super().move()
