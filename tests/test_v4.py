import numpy as np
probs={'A': [1, 0.1], 'B': [1, 0.1], 'C': [1, 0.1], 'D': [1, 0.1]}
xy=np.array([[1, 2], [2, 4]])
new_xv=np.zeros((np.size(xy, 0), np.size(xy, 1)))
for row_idx in range(0, np.size(new_xv, 0)):
    new_xv[row_idx, 0]=probs['A'][0]*xy[row_idx, 0]+probs['B'][0]*xy[row_idx, 1]
    new_xv[row_idx, 1]=probs['C'][0]*xy[row_idx, 0]+probs['D'][0]*xy[row_idx, 1]

print(new_xv)
