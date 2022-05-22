import multiprocessing
import os
import pickle
import monopoly.environment as env
import neat
import numpy as np

n = 1000

runs_per_net = 2

'''
network shape:
22 inputs / 21 outputs

input shape:
0: Balance
1: pos
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
11: railroads
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
21: railroads

output shape:
(in [0, 1])
0: buy?
1: trade?
(trade confidence ratios)
2: brown
3: skyblue
4: pink
5: orange
6: red
7: yellow
8: green
9: darkblue
10: companies
11: railroads

12: nHouses
(house buying confidence ratios)
13: brown
14: skyblue
15: pink
16: orange
17: red
18: yellow
19: green
20: darkblue
'''

class ParallelEvaluator(object):
    def __init__(self, num_workers, timeout=None, maxtasksperchild=None):
        self.timeout = timeout
        self.pool = multiprocessing.Pool(processes=num_workers, maxtasksperchild=maxtasksperchild)

    def __del__(self):
        self.pool.close()
        self.pool.join()
        self.pool.terminate()

    def evaluate(self, genomes, config):
        genomes_dict = {}
        for gen_id, genome in genomes:
            genome.fitness = 1
            genomes_dict[gen_id] = genome


        pool = multiprocessing.Pool(multiprocessing.cpu_count())

        duels = [[genomes[2*i], genomes[2*i + 1]] for i in range(int(len(genomes) / 2))]
        print(duels)

        # population size is 128 = 2**7
        # so we can do 7 rounds of duels
        # each time a genome goes to the next round,
        # its fitness is multiplied by 1.5
        for n in range(7):
            jobs = [pool.apply_async(env.play_a_game, (duel[0], duel[1], config)) for duel in duels]

            winners = [job.get() for job in jobs]

            for gen_id, genome in winners:
                # modified version of the sigmoid function
                genomes_dict[gen_id].fitness = 1 / (1 + np.exp(-n + 3.5))*100

            duels = [[winners[2*i], winners[2*i + 1]] for i in range(int(len(winners) / 2))]

        genomes = list(genomes_dict.items())


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
        pop = neat.Checkpointer.restore_checkpoint('neat-checkpoint-988')
    except:
        # create a new population from scratch
        pop = neat.Population(config)

    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.Checkpointer(100, filename_prefix='neat-checkpoint-'))

    pe = ParallelEvaluator(multiprocessing.cpu_count())
    winner = pop.run(pe.evaluate, n)


    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)


if __name__ == '__main__':
    run()