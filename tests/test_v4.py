import numpy as np
probs={'A': [1, 0.1], 'B': [1, 0.1], 'C': [1, 0.1], 'D': [1, 0.1]}
xy=np.array([[1, 2], [2, 4]])
xy_dev=np.array([[.1, .2], [.2, .4]])
new_xv=np.zeros((np.size(xy, 0), np.size(xy, 1)))
new_xv_dev=np.zeros((np.size(xy_dev, 0), np.size(xy_dev, 1)))

# mean value computation
for row_idx in range(0, np.size(new_xv, 0)):
    new_xv[row_idx, 0]=probs['A'][0]*xy[row_idx, 0]+probs['B'][0]*xy[row_idx, 1]
    new_xv[row_idx, 1]=probs['C'][0]*xy[row_idx, 0]+probs['D'][0]*xy[row_idx, 1]

# deviation computation
for row_idx in range(0, np.size(new_xv_dev, 0)):
    new_xv_dev[row_idx, 0]=probs['A'][1]**2*xy_dev[row_idx, 0]**2+probs['B'][1]**2*xy_dev[row_idx, 1]**2
    new_xv_dev[row_idx, 1]=probs['C'][1]**2*xy_dev[row_idx, 0]**2+probs['D'][1]**2*xy_dev[row_idx, 1]**2
print(new_xv)
print(new_xv_dev)
