# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Causal Inference
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import argparse

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
    None



