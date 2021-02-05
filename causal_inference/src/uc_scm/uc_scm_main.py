from causal_inference.src.uc_scm.scm import *

class service_scm(object):
    def __init__(self):
        None
    def test(self):
        obj=scm_class()
        problem = {'initial_state': [0, 1, 1.295], 'variables': {'000': 'x', '001': 'v', '002': 'a', '003': 'F'},
                   'scm': {'000': 'x+T*v', '001': 'v+T*a', '002': 'a+T*F', '003': 'F'}, 'parameters': {'000': 'T'}}
        topology=obj.get_topology_by_scm(problem)
        all_exp, all_var=obj.get_scm_function(problem, [1, 2, 3, 4])
        None


