import random
import matplotlib.pyplot as plt


class instance_of_RFCA():
    """
    This class implements a Random Function Cellular Automata. This is combination between a classic 1d cellular automata
    and a random boolean network. Each node of the cellular automoata uses its two neighbours in combination with a random
    boolean expression e.g. X and notY or Z where X,Y,Z are the contents of the node and its neighbours.
    """
    def __init__(self):
        #random starting nodes
        self.start_nodes = random.choices([True, False], k=30)
        self.generations = []
        #generate rules for all nodes
        self.node_rules = [self.generate_random_boolean_expression() for x in range(30)]      
        self.update = True
        self.generation_count = 0
        self.cycle_length = 0
        self.frozen_node_count = 0
        self.attractor_cycle = []


    #generates a random boolean expression for a node in the RFCA
    def generate_random_boolean_expression(self):
        operators = random.choices([' and ', ' or '], k = 2)
        not_or_not = random.choices(['not', ''], k = 3)
        expression = [operators, not_or_not]
        return(expression)


    #update individual node
    def update_node(self, left, node, right, node_rule):
        #apply not values
        if node_rule[1][0] == 'not':
            left = not left
        if node_rule[1][1] == 'not':
            node = not node
        if node_rule[1][2] == 'not':
            right = not right
        
        #apply operators
        if node_rule[0][0] == ' and ' and node_rule[0][1] == ' or ':
            modified_node = left and node or right
        elif node_rule[0][0] == ' and ' and node_rule[0][1] == ' and ':
            modified_node = left and node and right
        elif node_rule[0][0] == ' or ' and node_rule[0][1] == ' and ':
            modified_node = left or node and right
        elif node_rule[0][0] == ' or ' and node_rule[0][1] == ' or ':
            modified_node = left or node or right

        return(modified_node)
        

    def get_attractor_cycle_length(self, gen):
        if gen in self.generations:
            self.cycle_length = (len(self.generations)) - self.generations.index(gen)
            return self.cycle_length
        else:
            return -1


    #move forward a generation
    def update_nodes(self, nodes):
        updated_nodes_count = 0
        new_gen = []
        for x in nodes:
            new_gen.append(self.update_node(nodes[(updated_nodes_count-1) % 30], x, nodes[(updated_nodes_count+1) % 30], self.node_rules[updated_nodes_count]))
            updated_nodes_count += 1
        self.cycle_length = self.get_attractor_cycle_length(new_gen)
        self.generations.append(new_gen)
        if self.cycle_length != -1:
            self.get_number_of_frozen_nodes(new_gen)
            return False
        else:
            return True

    def plot_space_time_graph(self):
        full_plot = []
        for x in range(len(self.generations)-self.cycle_length):
            full_plot.append(self.generations[x])
        full_plot.pop()
        for p in 1,2:
            for x in self.attractor_cycle:
                gen = []
                for y in x:
                    if y == True:
                        gen.append(2)
                    else:
                        gen.append(3)
                full_plot.append(gen)
        
        plt.pcolor(full_plot)
        plt.show()


    
    def get_number_of_frozen_nodes(self, gen):
        self.attractor_cycle = self.generations[self.generations.index(gen):len(self.generations)]
        i = 0
        for x in gen:
            frozen = True
            for y in self.attractor_cycle:
                if x != y[i]:
                    frozen = False
            if frozen == True:
                self.frozen_node_count += 1
            i += 1


    def run_instance(self):
        self.update = True
        self.generation_count = 0
        self.cycle_length = 0
        self.frozen_node_count = 0
        self.attractor_cycle = []
        self.generations = [self.start_nodes]
        while self.update == True:
            self.update = self.update_nodes(self.generations[self.generation_count])
            self.generation_count += 1