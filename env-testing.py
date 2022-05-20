import monopoly.environment as env
import multiprocessing
import os
import pickle

import neat
import numpy as np

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)


observation = env.reset()
pop = neat.Population(config)
gen1 = pop.population[1]
gen2 = pop.population[2]
net1 = neat.nn.FeedForwardNetwork.create(gen1, config)
net2 = neat.nn.FeedForwardNetwork.create(gen2, config)




print(observation)
print()
env.play_a_game(net1, net2)
'''
done = False
while not done:
    observation, reward, done, info = env.step(env.action_space.sample())
'''