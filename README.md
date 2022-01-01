# Novelty_Search_on_RFCA
This is a domain specific implementation of a novelty search on a Random Function Cellular Automata (see RFCA.py for explanation)
it takes the parameters of cycle length and number of frozen nodes in a cycle and plots them on a XY axis. It then searches the
state space by comparing two nodes on their novelty (implemented as a node's average distance from its n nearest neghbours).
The loosing node is mutated using the winner to encourage evolution towards more novel nodes. If a winning node is novel enough when
being compared it is added to an archive, this allows us to see a path through the state space as the search progresses.

# RFCAs (Random Function Cellular Automata)
RFCAs are a combination between a classic 1d cellular automata and a random boolean network. 
Each node of the cellular automoata uses its two neighbours in combination with a random
boolean expression e.g. X and notY or Z where X,Y,Z are the contents of the node and its neighbours.
