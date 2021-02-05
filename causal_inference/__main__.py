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
    parser.add_argument('--sample_time', '-Ts', type=float, help='Ts=0.1',
                        default='0.1', required=False)
    args = parser.parse_args()
    params = vars(args)
    ########################
    ### Causal Inference ###
    ########################
    obj = service_scmMDP()
    obj.show_graph()

    t = obj.problem.obj_solver.get_scm_function(obj.problem.obj_solver.data,
                                                [Normal('x', 1.295, 0.273), Normal('v', 1.295, 0.273),
                                                 Normal('v', 1.295, 0.273)])
    print(t)
    t = obj.problem.obj_solver.get_scm_function(obj.problem.obj_solver.data,
                                                [3, 4,
                                                 Normal('v', 1.295, 0.273)])
    print(t)



