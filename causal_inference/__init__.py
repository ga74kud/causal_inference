# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Causal Inference
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

from causal_inference.src.uc_scm.scm import *

''' 
Get the solution for the Structural Causal Model (SCM)
'''
def get_scm_solution(problem, input):
    obj = scm_class()
    # topology=obj.get_topology_by_scm(problem)
    all_exp, all_var = obj.get_scm_function(problem, input)
    return all_exp, all_var