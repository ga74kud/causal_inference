import causal_inference as ci
import numpy as np
probs={'A': {"mean": 1, "dev": 1}, 'B': {"mean": 1, "dev": 0.1}, 'C': {"mean": 1, "dev": 0.1}, 'D': {"mean": 1, "dev": 0.1}}
x={"mean": 1, "dev": .1}
y={"mean": 2, "dev": .2}
xy=[x, y]
new_xv=ci.next_position_scm(xy, probs)
print(new_xv)
