from abc import ABC, abstractmethod
from time import time

class GridWorld:
    def __init__(self, size, home_location):
        self.size = size
        self.walls = set()
        self.points_of_interest = set()
        self.home_location = home_location
        self.home_base = HomeBase(self, *home_location)
        self.reset()

    def reset(self):
        self.points_of_interest_found = set()
        self.agents = []
        self.points_of_interest_found_times = []
        self.start_time = time()

    def seed_agents(self, agent_class, number_of_agents):
        for _ in range(number_of_agents):
            self.agents.append(agent_class(self, *self.home_location))

    @staticmethod
    def load_walls(filename):
        walls = set()
        with open(filename) as f:
            for line in f:
                if line.strip():
                    y, xs = line.strip().split()
                    xs = xs.split(',')
                    y = int(y)
                    for x in xs:
                        walls.add((int(x), y))
        return walls

    def add_walls(self, walls, offsetx, offsety):
        self.walls |= {(offsetx + x, offsety + y) for x, y in walls}

    def generate_walls(self):
        self.draw_border(0, 0, self.size, self.size)

    def draw_border(self, x1, y1, x2, y2):
        for i in range(x1, x2 + 1):
            self.walls.add((i, y1))
            self.walls.add((i, y2))
        for j in range(y1, y2 + 1):
            self.walls.add((x1, j))
            self.walls.add((x2, j))

    def get_cell(self, agent, dx, dy):
        if dx not in {-1, 0, 1} or dy not in {-1, 0, 1}:
            raise ValueError('vector too large', dx, dy)
        x = agent.x + dx
        y = agent.y + dy
        pos = (x, y)
        if self.home_location == pos:
            return 'home'
        if pos in self.points_of_interest:
            return 'target'
        if pos in self.walls:
            return 'wall'
        return 'empty'

    def get_nearby_agents(self, agent):
        return [a for a
                in self.agents
                if a is not agent
                and abs(a.x - agent.x) <= 1
                and abs(a.y - agent.y) <= 1]

    def step(self):
        for agent in self.agents:
            dx, dy = agent.move()
            if dx not in {-1, 0, 1} or dy not in {-1, 0, 1}:
                raise ValueError('vector too large', dx, dy)
            if self.get_cell(agent, dx, dy) == 'wall':
                raise ValueError('cannot run into wall')
            agent.x += dx
            agent.y += dy
            pos = (agent.x, agent.y)
            if pos in self.points_of_interest:
                if pos not in self.points_of_interest_found:
                    self.points_of_interest_found.add(pos)
                    self.points_of_interest_found_times.append(time() - self.start_time)

    def run(self, number_of_steps):
        for _ in range(number_of_steps):
            self.step()
        return len(self.points_of_interest_found)


class Agent(ABC):
    def __init__(self, world, x, y):
        self.map = {}
        self.world = world
        self.x = x
        self.y = y

    def sync_map(self, other):
        newmap = {}
        for key in self.map.keys() - other.map.keys():
            newmap[key] = self.map[key]
        for key in other.map.keys() - self.map.keys():
            newmap[key] = other.map[key]
        for key in self.map.keys() & other.map.keys():
            v1 = self.map[key]
            v2 = self.map[key]
            newmap[key] = min(v1, v2)
        self.map = newmap
        other.map = newmap.copy()

    @abstractmethod
    def move(self):
        pass  # implement this


class HomeBase(Agent):
    def move(self):
        return 0, 0
