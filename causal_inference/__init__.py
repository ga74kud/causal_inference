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
def product_two_gaussians(gaus_1, gaus_2):
    mu_1 = gaus_1["mean"]
    mu_2 = gaus_2["mean"]
    dev_1 = gaus_1["dev"]
    dev_2 = gaus_2["dev"]
    new_mean=(mu_1/(2*dev_1**2)+mu_2/(2*dev_2**2))/(1/(2*dev_1**2)+1/(2*dev_2**2))
    dev=(dev_1 ** 2 * dev_2**2)/(dev_1 ** 2 + dev_2**2)
    gaus={"mean": new_mean, "dev": np.sqrt(dev)}
    return gaus
def sum_two_gaussians(gaus_1, gaus_2):
    mu_1 = gaus_1["mean"]
    mu_2 = gaus_2["mean"]
    dev_1 = gaus_1["dev"]
    dev_2 = gaus_2["dev"]
    new_mean=mu_1+mu_2
    dev=dev_1 ** 2 * dev_2**2
    gaus={"mean": new_mean, "dev": np.sqrt(dev)}
    return gaus
def next_position_scm(xy, probs):
    # x-coordinate
    prod_1 = product_two_gaussians(probs['A'], xy[0])
    prod_2 = product_two_gaussians(probs['B'], xy[0])
    new_x = sum_two_gaussians(prod_1, prod_2)
    # y-coordinate
    prod_3 = product_two_gaussians(probs['C'], xy[1])
    prod_4 = product_two_gaussians(probs['D'], xy[1])
    new_y = sum_two_gaussians(prod_3, prod_4)
    new_xy=[new_x, new_y]
    return new_xy