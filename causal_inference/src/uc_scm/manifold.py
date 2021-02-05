import numpy as np


class manifold(object):
    def __init__(self, **kwargs):
        self.manifold= {'X': None, 'Topology': [], 'Adjacency': None, 'amount_states': None,
                        'Actions': {}, 'Position': None}
        self.param={'option_topology': 'const_neigh', 'neighbour_distance': 1.2}




if __name__ == '__main__':
    obj=manifold()
    obj.set_environment()
    print(obj.manifold)