# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Causal Inference
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
from causal_inference.src.uc_scm.uc_scm_main import *
import argparse
from sympy.stats import *
from __init__ import *
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ##################
    ### Parameters ###
    ##################
    parser = argparse.ArgumentParser()
    # parser.add_argument('--sample_time', '-Ts', type=float, help='Ts=0.1',
    #                     default='0.1', required=False)
    args = parser.parse_args()
    params = vars(args)
    ########################
    ### Causal Inference ###
    ########################
    obj = service_scm()
    problem = {'variables': {'000': 'V', '001': 'F'},
               'scm': {'000': 'V', '001': '2*V+F'}}
    input=[[1, .1], [2, 0.1]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ]
    all_exp, all_var = get_solution(problem, input)
    print(all_exp)
    print(all_var)



