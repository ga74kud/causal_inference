import __init__
from causal_inference.src.uc_scm.scm import *

class service_scm(object):
    def __init__(self):
        None
    def test(self):
        obj=scm_class()
        problem = {'variables': {'000': 'x', '001': 'v', '002': 'a', '003': 'F'},
                   'scm': {'000': 'x+v+a', '001': 'v', '002': 'a', '003': 'F'}}
        #topology=obj.get_topology_by_scm(problem)
        all_exp, all_var=obj.get_scm_function(problem, [[1, .1], [2, 0.1], [3, 0.1], [4, 0.1]])

        all_exp, all_var=get_solution(problem, input)
        print(all_exp)
        print(all_var)
        None


