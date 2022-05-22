import os
import pickle
import neat
import monopoly.environment as env
import numpy as np

try:
    # load the winner
    with open('winner', 'rb') as f:
        c = pickle.load(f)
except:
    # load the best genome of the last checkpoint
    loaded_pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-1679')

    c = loaded_pop.best_genome

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)



observation = env.reset()
Lwinner = []
for _ in range(1):
    try:
        pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-988')
        print('POPULATION LOADED')

    except:
        print('GENERATE A NEW POPULATION')
        pop = neat.Population(config)
    for gen in pop.population.items():
        winner = env.play_a_game((1, c), gen, config)
        print(winner)
        Lwinner.append(winner[0])

print(f'\nWin rate :{Lwinner.count(1) / len(Lwinner)}')