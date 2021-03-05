import causal_inference as ci
import numpy as np
probs={'a': 2, 'b': 4, 'c': 3, 'd': 1}
X={"mean": 0, "dev": 1}
Y={"mean": 0, "dev": 1}
XY=[X, Y]
X, Y, VX, VY=ci.next_position_scm(XY, probs)

print(X, Y, VX, VY)
