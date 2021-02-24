from sklearn.decomposition import PCA
import md_pro as md
import numpy as np
import matplotlib.pyplot as plt

def plot_nodes(P, **kwargs):
    fig, ax = plt.subplots()
    all_points=np.array([P[p] for p in P])
    ax.scatter(all_points[:, 0], all_points[:, 1], c=kwargs["U"])
    for i, txt in enumerate(P):
        ax.annotate(txt, (all_points[i, 0], all_points[i, 1]))


mygrid={"x_grid": 5, "y_grid": 4}
amount_nodes=np.int(mygrid["x_grid"]*mygrid["y_grid"])

#start point
strt_pnt='0'
# points
P=md.get_meshgrid_points(**mygrid)
# Topology
T, S = md.get_simple_topology_for_regular_grid(P, **mygrid)
# rewards
R = {'16': 100}
mdp_challenge = {'S': S, 'R': R, 'T': T, 'P': P, 'gamma': .9}
# start Markov Decision Process
dict_mdp=md.start_mdp(mdp_challenge)
# plot the nodes
plot_nodes(P, **{'U': dict_mdp['U']})
plt.show()