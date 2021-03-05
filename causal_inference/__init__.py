# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Causal Inference
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
import numpy as np
from causal_inference.src.uc_scm.scm import *

''' 
Get the solution for the Structural Causal Model (SCM)
'''
def get_scm_solution(problem, input):
    obj = scm_class()
    # topology=obj.get_topology_by_scm(problem)
    all_exp, all_var = obj.get_scm_function(problem, input)
    return all_exp, all_var

def next_position_scm(XY, probs):
    X = XY[0]
    Y = XY[1]
    VX = {"mean": probs['a']*X['mean'] + probs['b']*Y['mean'], "dev": (probs['a']**2)*(X['dev']**2) + (probs['b']**2)*(Y['dev']**2)}
    VY = {"mean": probs['c']*X['mean'] + probs['d']*Y['mean'], "dev": probs['c']**2*X['dev']**2 + probs['d']**2*Y['dev']**2}
    return X, Y, VX, VY
