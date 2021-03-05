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
    VX = {"mean": probs['A']*X['mean'] + probs['B']*Y['mean'], "dev": (probs['A']*X['dev'])**2 + (probs['B']*Y['dev'])**2}
    VY = {"mean": probs['C']*X['mean'] + probs['D']*Y['mean'], "dev": (probs['C']*X['dev'])**2 + (probs['D']*Y['dev'])**2}
    return X, Y, VX, VY