import causal_inference as ci
import numpy as np
probs={'A': [1, 0.1], 'B': [1, 0.1], 'C': [1, 0.1], 'D': [1, 0.1]}
xy={"mean": np.array([[1, 2], [2, 4]]), "dev": np.array([[.1, .2], [.2, .4]])}

new_xv=ci.next_position_scm(xy, probs)
print(new_xv["mean"])
print(new_xv["dev"])
