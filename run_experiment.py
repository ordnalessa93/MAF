from gridworld import GridWorld
from agent import MAFAgent, IMAFAgent
import os
from random import randint, choice, random
from itertools import cycle, islice
from pathlib import Path
import simplejson as json
import time

SIZE = 500
NUMBER_OF_AGENTS = 20
NUMBER_OF_STEPS = SIZE * SIZE
POINTS_OF_INTEREST = 15 if SIZE == 1000 else 10
EDGES = (1, SIZE - 1)


def run_single_experiment(house):
    x = choice(EDGES)
    y = randint(*EDGES)
    if random() < .5:
        x, y = y, x
    home_base = (x, y)
    world = GridWorld(1000, home_base)
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
    start_time_a = time.time()
    a = world.run(NUMBER_OF_STEPS)
    end_time_a = time.time()
    elapsed_time_a = end_time_a - start_time_a
    
    a_ft = world.points_of_interest_found_times
    world.reset()
    world.seed_agents(IMAFAgent, NUMBER_OF_AGENTS)
    start_time_b = time.time()
    b = world.run(NUMBER_OF_STEPS)
    end_time_b = time.time()
    elapsed_time_b = end_time_b - start_time_b

    b_ft = world.points_of_interest_found_times
    return {'MAF': {'targets_saved': a, 'find_times': a_ft, 'elapsed_time_MAF': elapsed_time_a}, 'IMAF': {'targets_saved': b, 'find_times': b_ft, 'elapsed_time_IMAF': elapsed_time_b}}

def get_output_filename():
    i = 1
    while True:
        p = Path(f'raw-results-{i}.json')
        if not p.exists():
            return p
        i += 1

if __name__ == '__main__':
    houses = []
    for house in os.listdir('world-data'):
        houses.append((house, GridWorld.load_walls('world-data/' + house)))
    with get_output_filename().open('w') as f:
        f.write('[')
        f.flush()
        try:
            for i, (housename, house) in enumerate(islice(cycle(houses), len(houses) * 100)):
                results = run_single_experiment(house)
                if i > 0:
                    f.write(',\n')
                f.write(json.dumps({'world': housename, 'results': results}))
                f.flush()
                print(f'exp {i} (world: {housename}) complete')
        finally:
            f.write(']')
            f.flush()
    print('all experiments complete')
