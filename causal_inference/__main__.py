# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Causal Inference
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
import argparse
from sympy.stats import *
from __init__ import *
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    ########################
    ### Causal Inference ###
    ########################
    problem = {'variables': {'000': 'x', '001': 'y'},
               'scm': {'000': 'a*x+b*y', '001': 'c*x+d*y'}}
    input=[[1, .1], [2, 0.1]]
    all_exp, all_var = get_scm_solution(problem, input)
    print(all_exp)
    print(all_var)




