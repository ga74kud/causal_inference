import causal_inference
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt

def neighbour_id(A, id):
    neigh=A[id]
    neigbours=[idx for idx, val in enumerate(neigh) if val]
    return neigbours

def find_next_node(A, id, V):
    neigh_id = neighbour_id(A, id)
    values=[V[i] for i in neigh_id]
    idx=np.argmax(values)
    return neigh_id[idx]

nodes_amount=10
value_fcn_level=100
colors = plt.cm.jet(np.linspace(0,1,value_fcn_level))
g = ig.Graph.GRG(nodes_amount, 2)
V=np.random.choice(value_fcn_level, nodes_amount)
plot_colors=[(colors[i,0], colors[i,1], colors[i,2]) for i in V]
g.vs["color"] = plot_colors
# g.vs["label"] = [str(idx)+"/"+str(val) for idx, val in enumerate(V)]
visual_style = {}
visual_style["vertex_label"]=[str(idx)+"/"+str(val) for idx, val in enumerate(V)]
visual_style["vertex_label_size"]=40
visual_style["margin"] = 60
A=g.get_adjacency()
next_node=2
for wlt in range(0, 3):
    next_node=find_next_node(A, next_node, V)
    print("wlt="+str(wlt)+": "+ str(next_node))
# print(A)
#
ig.plot(g, **visual_style)

r=1
None