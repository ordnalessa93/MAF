from gridworld import GridWorld
from agent import MAFAgent, IMAFAgent

import os
import sys
import numpy as np
from random import randint, choice, random
from itertools import cycle, islice
from pathlib import Path
import json
import time


def run_single_experiment(house):
    x = choice(EDGES)
    y = randint(*EDGES)
    if random() < .5:
        x, y = y, x
    home_base = (x, y)
    world = GridWorld(SIZE, home_base)
    world.generate_walls()
    world.add_walls(house, 0, 0)
    for _ in range(POINTS_OF_INTEREST):
        while True:
            p = (randint(1, SIZE - 1), randint(1, SIZE - 1))
            if (p != home_base and p not in world.walls
               and p not in world.points_of_interest):
                world.points_of_interest.add(p)
                break
    world.seed_agents(MAFAgent, NUMBER_OF_AGENTS)
    start_time = time.time()
    a = world.run(NUMBER_OF_STEPS)
    end_time = time.time()
    time_elapsed_a = end_time - start_time
    a_ft = world.points_of_interest_found_times
    world.reset()
    world.seed_agents(IMAFAgent, NUMBER_OF_AGENTS)
    start_time = time.time()
    b = world.run(NUMBER_OF_STEPS)
    end_time = time.time()
    time_elapsed_b = end_time - start_time
    b_ft = world.points_of_interest_found_times
    return {'MAF': {'targets_saved': a, 'find_times': a_ft, 'time_elapsed': time_elapsed_a}, 'IMAF': {'targets_saved': b, 'find_times': b_ft, 'time_elapsed': time_elapsed_b}}


houses = []
for house in os.listdir('world-data'):
  houses.append((house, GridWorld.load_walls('world-data/' + house)))


for h, house in houses:
  if h == 'blank.txt': break

testname = sys.argv[2]

def get_output_filename(vary, value):
    return Path(f'test-results-{testname}-{vary}-{value}.json')

arg = sys.argv[1]
if arg == 'size':
    # change the size of the map
    sizes_array = np.linspace(100, 500, 5)
    for size in sizes_array: 
      SIZE = int(size)
      NUMBER_OF_AGENTS = 10
      NUMBER_OF_STEPS = 25000
      POINTS_OF_INTEREST = 10
      EDGES = (1, SIZE - 1)

      with get_output_filename('size', SIZE).open('w') as f:
        f.write(json.dumps(run_single_experiment(house)))
elif arg == 'steps':
    # change the number of steps
    steps_array = np.linspace(1000, 50000, 10)
    for steps in steps_array: 
      SIZE = 200
      NUMBER_OF_AGENTS = 10
      NUMBER_OF_STEPS = int(steps)
      POINTS_OF_INTEREST = 10
      EDGES = (1, SIZE - 1)

      with get_output_filename('steps', NUMBER_OF_STEPS).open('w') as f:
        f.write(json.dumps(run_single_experiment(house)))
elif arg == 'agents':
    # change the number of agents
    agents_array = np.linspace(2, 20, 10)
    for agents in agents_array: 
      SIZE = 200
      NUMBER_OF_AGENTS = int(agents)
      NUMBER_OF_STEPS = 25000
      POINTS_OF_INTEREST = 10
      EDGES = (1, SIZE - 1)

      with get_output_filename('agents', NUMBER_OF_AGENTS).open('w') as f:
        f.write(json.dumps(run_single_experiment(house)))
elif arg == 'targets':
    # change the number of targets
    targets_array = np.linspace(2, 20, 10)
    for targets in targets_array: 
      SIZE = 200
      NUMBER_OF_AGENTS = 10
      NUMBER_OF_STEPS = 25000
      POINTS_OF_INTEREST = int(targets)
      EDGES = (1, SIZE - 1)

      with get_output_filename('targets', POINTS_OF_INTEREST).open('w') as f:
        f.write(json.dumps(run_single_experiment(house)))
else:
    print('please select one of size, steps, agents, targets')
