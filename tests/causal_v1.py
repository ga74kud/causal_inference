import causal_inference as ci
import numpy as np

start_pos = {'mu': np.array([0, 0]), 'Sigma': np.array([[.4, 0], [0, .4]])}
vel = {0: {'pi': .6, 'mu': np.array([8, 8]), 'Sigma': np.array([[1, 0.5], [0.5, 1]])},
       1: {'pi': .3, 'mu': np.array([-8, 2]), 'Sigma': np.array([[.4, -0.6], [-0.6, .4]])},
       2: {'pi': .1, 'mu': np.array([1, -7]), 'Sigma': np.array([[.4, -0.6], [-0.6, .4]])}
       }
xh = np.array([5, 5])

input={"start_pos": start_pos, "vel": vel, "N": 600, "xh": xh}
ci.get_observational_interventional_targets(**input)