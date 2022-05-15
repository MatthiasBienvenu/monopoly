import os
import pickle
import neat
import gym 
import numpy as np

try:
    # load the winner
    with open('winner', 'rb') as f:
        c = pickle.load(f)
except:
    # load the best genome of the last checkpoint
    pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-2').population
    i = max(pop.keys())
    c = pop[i]

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config_monopoly')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)


env = gym.make("BipedalWalker-v3")
observation = env.reset()

done = False
while not done:
    action = net.activate(observation)

    observation, reward, done, info = env.step(action)
    env.render()