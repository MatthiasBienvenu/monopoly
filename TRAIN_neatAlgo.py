import multiprocessing
import os
import pickle

import neat
import numpy as np
import gym

n = 100

runs_per_net = 2

'''
network shape:
21 inputs / 20 outputs

input shape:
1: Balance
(group position 0 or 1)
2: brown
3: skyblue
4: pink
5: orange
6: red
7: yellow
8: green
9: darkblue
10: companies
11: Lrailroads
(possessed ratios in [0, 1])
12: brown
13: skyblue
14: pink
15: orange
16: red
17: yellow
18: green
19: darkblue
20: companies
21: Lrailroads

output shape:
(in [0, 1])
1: buy?
2: trade?
(trade confidence ratios)
3: brown
4: skyblue
5: pink
6: orange
7: red
8: yellow
9: green
10: darkblue
11: companies
12: Lrailroads

13: nHouses
(house buying confidence ratios)
14: brown
15: skyblue
16: pink
17: orange
18: red
19: yellow
20: green
21: darkblue
'''

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []

    for runs in range(runs_per_net):
        env = gym.make("BipedalWalker-v3")

        observation = env.reset()
        fitness = 0.0
        done = False
        while not done:

            action = net.activate(observation)
            observation, reward, done, info = env.step(action)
            fitness += reward

        fitnesses.append(fitness)

    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    try:
        # load the last checkpoint
        pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-2')
    except:
        # create a new population from scratch
        pop = neat.Population(config)

    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.Checkpointer(10, filename_prefix='neat-checkpoint-'))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, n)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)


if __name__ == '__main__':
    run()