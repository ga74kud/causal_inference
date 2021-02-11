import causal_inference
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt


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
ig.plot(g, **visual_style)