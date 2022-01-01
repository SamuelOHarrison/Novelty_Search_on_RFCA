import random
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
import numpy as np
from RFCA import instance_of_RFCA

class novelty_search():
    """
    This is a domain specific implementation of a novelty search on a Random Function Cellular Automata (see RFCA.py for explanation)
    it takes the parameters of cycle length and number of frozen nodes in a cycle and plots them on a XY axis. It then searches the
    state space by comparing two nodes on their novelty (implemented as a node's average distance from its n nearest neghbours).
    The loosing node is mutated using the winner to encourage evolution towards more novel nodes. If a winning node is novel enough when
    being compared it is added to an archive, this allows us to see a path through the state space as the search progresses.
    """
    def __init__(self, initial_novelty_threshold, population_count, no_cycles):
        self.archive = []
        self.novelty_threshold = initial_novelty_threshold
        self.population_count = population_count
        self.no_cycles = no_cycles
        self.novelty_count = 0
        self.population = {}
        self.before_frozen = []
        self.before_cycles = []
        self.frozen_nodes = []
        self.cycle_lengths = []
        self.archive_frozen = []
        self.archive_cycle = []
        self.highest_cycle = 0
        self.last_archive_length = 1
        self.previous_archive_length = 0



    def generate_population(self, pop_count):
        for x in range(pop_count):
            RFCA = instance_of_RFCA()
            RFCA.run_instance()
            self.population[x] = [RFCA.node_rules, RFCA.frozen_node_count, RFCA.cycle_length, RFCA]

    
    def get_nearest_neighbours_full(self, individual, index):
        archive = np.zeros((len(self.archive),2))
        for x in range(len(self.archive)):
            archive[x][0] = self.archive[x][0][1]
            archive[x][1] = self.archive[x][0][2]
        archive[-1][0] = individual[1]
        archive[-1][1] = individual[2]
        if len(archive) < 10:
            n = len(archive)
        else:
            n = 10
        nbrs = NearestNeighbors(n_neighbors=n, algorithm='kd_tree').fit(archive)
        distances, indices = nbrs.kneighbors(archive)
        return (distances[-1])

    def get_novelty(self, individual, index):
        #returns novelty as the avg distance from closest 10 members of the archive
        if len(self.archive) < 1:
            self.novelty_count +=1
            return self.novelty_threshold
        else:
            distances = self.get_nearest_neighbours_full(individual, index)
            distance = 0
            for x in distances:
                distance += x
            distance = distance/len(distances)
            if distance < 1.5: 
                distance = 1.5
            self.novelty_count += 1
            return distance

    def update_novelty_threshold(self, n):
        if len(self.archive) == self.previous_archive_length:
            self.novelty_threshold = self.novelty_threshold * .80
        else:
            percentage_increase = ((len(self.archive) - self.previous_archive_length)/n)
            self.novelty_threshold = self.novelty_threshold * (1 + percentage_increase*2)

        self.previous_archive_length = len(self.archive)


    def mutate(self, winner, loser):
        index = random.randint(0, 14)
        loser[0][index:index+15] = winner[0][index:index+15]
        for i in range(len(winner[0])):
            random_number = random.randint(0,100)
            if random_number <= 1:
                loser[3].node_rules[i] = loser[3].generate_random_boolean_expression()
                winner[3].node_rules[i] = winner[3].generate_random_boolean_expression()

    def plot(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        ax1.scatter(self.frozen_nodes, self.cycle_lengths, c='blue', label='General Population')
        ax1.scatter(self.archive_frozen, self.archive_cycle, c='red', label='Archive')
        plt.legend(loc='upper right')
        plt.show()



    def run(self):
        self.generate_population(self.population_count)
        self.population_array = np.zeros((self.population_count, 2))
        for x in self.population:
            self.before_frozen.append(self.population[x][1])
            self.before_cycles.append(self.population[x][2])
            self.population_array[x][0] = self.population[x][1]
            self.population_array[x][1] = self.population[x][2]
            if self.population[x][2] > self.highest_cycle:
                self.highest_cycle = self.population[x][2]

        self.y_axis_normalising_constant = self.highest_cycle/30
        while self.novelty_count < self.no_cycles:
            #update novelty threshold every 50 runs (there are 2 novelty counts per cycle)
            if self.novelty_count % 100 == 0 and self.novelty_count != 0:
                self.update_novelty_threshold(50)
                    
            #Get two random individuals in the population
            index_1, index_2 = random.randint(0,len(self.population)-1), random.randint(0,len(self.population)-1)
            while index_1 == index_2:
                index_2 = random.randint(0,len(self.population)-1)
            #find the novelty of both individuals
            novelty_1 = self.get_novelty(self.population[index_1], index_1)
            novelty_2 = self.get_novelty(self.population[index_2], index_2)
            
            for x in index_1,index_2:
                self.frozen_nodes.append(self.population[x][1])
                self.cycle_lengths.append(self.population[x][2])
            

            if novelty_1 >= novelty_2:
                index = (index_1, index_2)
                novelty = novelty_1
            else:
                index = (index_2, index_1)
                novelty = novelty_2

            self.mutate(self.population[index[0]], self.population[index[1]])
            #re-run mutated RFCA
            self.population[index[1]][3].run_instance()
            self.population[index[1]][1], self.population[index[1]][2]  = self.population[index[1]][3].frozen_node_count, self.population[index[1]][3].cycle_length
            self.population_array[index[1]][0], self.population_array[index[1]][1]  = self.population[index[1]][3].frozen_node_count, self.population[index[1]][3].cycle_length
            #add winner to archive if needed
            if novelty >= self.novelty_threshold:
                archiveable = [self.population[index[0]], novelty, index[0]]
                self.archive.append(archiveable)
            
        for i in self.archive:
            self.archive_frozen.append(i[0][1])
            self.archive_cycle.append(i[0][2])
            



search = novelty_search(1000, 1000, 100000)
search.run()
search.plot()