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

def next_position_scm(xy, probs):
    new_xv = {"mean": np.zeros((np.size(xy["mean"], 0), np.size(xy["mean"], 1))),
              "dev": np.zeros((np.size(xy["dev"], 0), np.size(xy["dev"], 1)))}
    # mean value computation
    for row_idx in range(0, np.size(new_xv["mean"], 0)):
        new_xv["mean"][row_idx, 0] = probs['A'][0] * xy["mean"][row_idx, 0] + probs['B'][0] * xy["mean"][row_idx, 1]
        new_xv["mean"][row_idx, 1] = probs['C'][0] * xy["mean"][row_idx, 0] + probs['D'][0] * xy["mean"][row_idx, 1]

    # deviation computation
    for row_idx in range(0, np.size(new_xv["dev"], 0)):
        new_xv["dev"][row_idx, 0] = probs['A'][1] ** 2 * xy["dev"][row_idx, 0] ** 2 + probs['B'][1] ** 2 * xy["dev"][
            row_idx, 1] ** 2
        new_xv["dev"][row_idx, 1] = probs['C'][1] ** 2 * xy["dev"][row_idx, 0] ** 2 + probs['D'][1] ** 2 * xy["dev"][
            row_idx, 1] ** 2
    return new_xv