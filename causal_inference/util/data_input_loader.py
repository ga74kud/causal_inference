import json
import numpy as np
import warnings
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def get_from_json(input_file):
    f = open(input_file, "r")
    data = json.loads(f.read())
    return data
def read_json_point_list(input_dictionary):
    return np.array([i for i in input_dictionary.values()])

def map_for_queue(map):
    queue_list = []
    for idx, wlt in enumerate(map):
        queue_list.append({"actor_name": "map_"+str(idx), "to_plot": wlt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red"})
    return queue_list

def reach_for_queue(map, dict_reach, dict_mdp):
    act_reach=np.sort([int(wlt) for wlt in dict_reach[-1]])
    act_reach=act_reach.tolist()
    act_U_mdp=[dict_mdp["U"][wlt] for wlt in range(0, len(dict_mdp["S"]))]
    queue_list = []
    cmap = get_colormap("plasma")
    scale_fac=(np.size(cmap, 0)-1)/np.max(act_U_mdp)
    act_U_col_idx=[np.int(np.floor(wlt*scale_fac)) for wlt in act_U_mdp]
    #col_idx = np.floor(np.linspace(0, np.size(cmap, 0) - 1, len(act_reach)))
    for idx, wlt in enumerate(map):
        act_col=cmap[act_U_col_idx[idx]]
        if(idx in act_reach):
            queue_list.append({"actor_name": "reach_"+str(idx), "to_plot": wlt,
                           "opacity": .8, "point_size": 20, "render_points_as_spheres": True, "color": act_col, "type": "sphere"})
        else:
            queue_list.append({"actor_name": "reach_" + str(idx), "to_plot": wlt,
                               "opacity": .4, "point_size": 10, "render_points_as_spheres": True, "color": act_col, "type": "cone"})
    return queue_list

def perturb_by_random_vector(vec, scale_val):
    pertub_vec=np.random.rand(len(vec))*scale_val
    new_vec=vec+pertub_vec
    return new_vec

def delaunay_map_for_queue(map):
    queue_list = []
    for idx, wlt in enumerate(map):
        queue_list.append({"actor_name": "map" + str(idx), "to_plot": wlt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red"})
    return queue_list

def get_direction(act_idx, act_coord, map, mdp_dict):
    FLAG_IS_VALID=False
    act_node=mdp_dict["S"][act_idx]
    act_multi_pi=mdp_dict["multi_pi"][act_node]
    act_neighbours=[wlt["neighbour"] for wlt in act_multi_pi]
    if(len(act_neighbours)==0):
        return 0, 0, 0, 0, FLAG_IS_VALID
    act_difference = [wlt["difference"] for wlt in act_multi_pi]
    all_directions=[tuple(map[int(wlt),:]-act_coord) for wlt in act_neighbours]
    try:
        a=np.max(act_difference)
        scale_vec=act_difference/a
    except:
        warnings.warn(str(act_neighbours)+str(act_difference), Warning)

    neigh_idx=[mdp_dict["S"].index(act_neighbours[idx]) for idx in range(0, len(act_neighbours))]
    end_points=[tuple(map[qrt, :]) for qrt in neigh_idx]
    FLAG_IS_VALID=True
    return all_directions, act_difference, scale_vec, end_points, FLAG_IS_VALID


def get_next_node(act_idx, map, mdp_dict):
    act_node_idx=mdp_dict["S"].index(act_idx)
    start_point=map[act_node_idx, :]
    act_multi_pi=mdp_dict["multi_pi"][act_idx]
    act_neighbours=[wlt["neighbour"] for wlt in act_multi_pi]
    act_difference = [wlt["difference"] for wlt in act_multi_pi]
    max_idx=act_difference.index(max(act_difference))
    neigh_idx=[mdp_dict["S"].index(act_neighbours[idx]) for idx in range(0, len(act_neighbours))]
    all_end_points=[tuple(map[qrt, :]) for qrt in neigh_idx]
    best_end_point=all_end_points[max_idx]
    best_end_idx=neigh_idx[max_idx]
    return start_point, all_end_points, best_end_point, best_end_idx

def vectorfield_for_queue(map, mdp_dict):
    queue_list = []
    for idx, wlt in enumerate(map):
        all_directions, act_difference, scale_vec, end_points, FLAG_IS_VALID=get_direction(idx, wlt, map, mdp_dict)
        if(FLAG_IS_VALID):
            for idx, qrt in enumerate(all_directions):
                queue_list.append({"actor_name": "vecfld_" + str(idx), "start": wlt, "direction": qrt,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "red",
                               "scale": scale_vec[idx], "pointa": wlt, "pointb": end_points[idx]})
        else:
            continue
    return queue_list

def optimal_path_for_queue(map, mdp_dict, storyline):
    params = get_params()
    act_node = storyline["start_node"]
    queue_list = []
    start_point_list=[]
    act_node_list=[]
    for idx in range(0, params["mdp"]["simulation"]["number_cycles_to_reach_target"]):
        start_point, all_end_points, best_end_point, next_node=get_next_node(act_node, map, mdp_dict)
        start_point_list.append(start_point.tolist())
        act_node_list.append(int(act_node))
        act_node=mdp_dict["S"][next_node]
        act_difference=np.array(best_end_point) - start_point
        queue_list.append({"actor_name": "vecfld_" + str(idx), "start": start_point, "direction": act_difference,
                           "opacity": .5, "point_size": 10, "render_points_as_spheres": True, "color": "blue",
                       "scale": 3})

    new_act_node_list=[]
    new_start_point_list=[]
    count=0
    for idx, val in enumerate(act_node_list):
        if(act_node_list[idx]==act_node_list[idx+1]):
            count+=1
        new_act_node_list.append(val)
        new_start_point_list.append(start_point_list[idx])
        if(count>=1):
            break
    optimal_path_list = {"start_point": new_start_point_list, "act_node": new_act_node_list}
    return queue_list, optimal_path_list

def trajectory_for_queue(map, trajectory):
    queue_list=[]
    cmap=get_colormap("cividis")
    col_idx=np.floor(np.linspace(0, np.size(cmap, 0)-1, len(trajectory)))
    ball_size=np.linspace(12, 40, len(trajectory))
    for wlt in range(0, len(trajectory)):
        act_idx=trajectory[wlt]
        new_point=map[act_idx, :]
        crow=np.int(col_idx[wlt])
        queue_list.append({"actor_name": "mdp_traj"+str(wlt), "to_plot": new_point, "opacity": .8,
                           "render_points_as_spheres": True, "point_size": ball_size[wlt], "color": cmap[crow,:]})
    return queue_list

def get_colormap(colmap):
    cmap=plt.get_cmap(colmap).colors
    return np.array(cmap)


def write_to_json(input_file, input_data):
    json_object = json.dumps(input_data)
    with open(input_file, "w") as outfile:
        outfile.write(json_object)

def get_params():
    dirs=get_special_paths()
    FILE_DIR=dirs["ROOT_DIR"]+dirs["PARAMS"]
    return get_from_json(FILE_DIR)

def get_special_paths():
    return get_from_json("../../input/config/special_paths.json")

def chunks(input, k):
    n=int(np.floor(len(input)/k))
    test=[np.array(input[i:i+n]) for i in range(0, len(input), n)]
    return test
'''
Get the xy coordinates from the optimal path of the MDP. Interpolate the xy coordinates
'''
def get_result_trajectories_mdp(optimal_mdp, coordinates, folder_to_store):
    act_traj=list()
    for wlt in optimal_mdp:
        x = coordinates[wlt, 0]
        y = coordinates[wlt, 1]
        act_traj.append((x,y))
    interpolated_points, points=interpolate_traj(act_traj)
    return interpolated_points, points
'''
    Interpolation of the trajectory in xy coordinates
'''
def interpolate_traj(act_traj):
    plt.figure()
    param=get_params()
    x = [wlt[0] for wlt in act_traj]
    y = [wlt[1] for wlt in act_traj]
    points=np.vstack((x,y)).T
    # Linear length along the line:
    distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    distance = np.insert(distance, 0, 0) / distance[-1]

    # Interpolation for different methods:
    interpolations_methods = ['quadratic']
    alpha = np.linspace(0, 1, param["mdp"]["simulation"]["spline_interpolation"])

    interpolated_points = {}
    for method in interpolations_methods:
        interpolator = interp1d(distance, points, kind=method, axis=0)
        interpolated_points[method] = interpolator(alpha)
    return interpolated_points, points

def plot_traj(intervention_list, obj_visual, interpolated_points, points, folder_to_store, mean_val_list, with_intervention):

    interpol_points=interpolated_points["quadratic"]
    # original points provided by MDP
    plt.figure(obj_visual.number)
    for method_name, curve in interpolated_points.items():
        plt.plot(*curve.T, '-', alpha=1)
    plt.plot(*points.T, 'ok', label='original points', alpha=1)

    mean_vals = mean_val_list["mean_val"]
    velocs=[wlt[1] for wlt in mean_vals]
    cmap = get_colormap("plasma")
    col_idx = np.floor(np.linspace(0, np.size(cmap, 0) - 1, 101))
    col_idx_int=[int(wlt) for wlt in col_idx]
    topi=np.interp(velocs, (np.min(velocs), np.max(velocs)), (0, 100))
    topi=[np.int(wrt) for wrt in topi]
    indexes=mean_val_list["interpol_idx"]
    points_A= interpol_points[0:-1]
    points_B = interpol_points[1:]
    tangency=points_B-points_A
    tangency=np.concatenate((tangency, np.array([[0, 0]])), axis=0)

    for idx, wlt in enumerate(interpol_points):
        if(idx in indexes):
            idx2_all=[idx2 for idx2, wlt in enumerate(indexes) if wlt==idx]
            x_pos=wlt[0]
            y_pos=wlt[1]
            distance=np.linalg.norm(tangency[idx])
            x_dif=tangency[idx][0]/distance
            y_dif = tangency[idx][1]/distance
            for qrt in idx2_all:
                act_vel_idx=topi[qrt]
                act_col=cmap[col_idx_int[act_vel_idx], :]
                scale=1
                plt.arrow(x_pos, y_pos, scale*x_dif, scale*y_dif,
                    fc=act_col, ec='blue', alpha=.65, width=.4,
                    head_width=1.4, head_length=1)

    if(intervention_list["interpolated_point"]!=[]):
        plt.plot(intervention_list["interpolated_point"][0][0], intervention_list["interpolated_point"][0][1], 'xr', label='intervention', alpha=1)

    plt.grid()
    plt.axis([-11.5, 11.5, -11.5, 11.5])
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')
    sm = plt.cm.ScalarMappable(cmap="plasma", norm=plt.Normalize(vmin=np.min(velocs), vmax=np.max(velocs)))
    sm._A = []
    plt.colorbar(sm)

    if(with_intervention):
        plt.savefig(folder_to_store+"trajectory_with_intervention.png")
    else:
        plt.savefig(folder_to_store + "trajectory_without_intervention.png")
    #plt.show()

def get_cumultative_distance(folder_to_store, interpolated_points):
    interpolated_points=interpolated_points["quadratic"]
    x = interpolated_points[:, 0]
    y = interpolated_points[:, 1]
    t=np.linspace(0, 100, len(x))
    dx = x[1:] - x[:-1]
    dy = y[1:] - y[:-1]

    step_size = np.sqrt(dx ** 2 + dy ** 2)

    cum_dist = np.concatenate(([0], np.cumsum(step_size)))
    #plot_trajectory(folder_to_store, t, cum_dist, 't [%]', 'd [m]', "cumulative_path_length")
    return cum_dist

def plot_mean_value(folder_to_store, mean_val_list):
    x=[wlt[0] for wlt in mean_val_list["mean_val"]]
    t=np.linspace(0, len(x), len(x))
    #plot_trajectory(folder_to_store, t, x, 't [%]', 'x [m]', "mean_val")
def plot_trajectory(folder_to_store, t, y, xlab, ylab, name):
    plt.figure()
    plt.plot(t, y, alpha=.6)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.savefig(folder_to_store+name+".png")

def intersect(lstA, lstB):
    return [val for val in lstA if val in lstB]

def union_of_lists(lstA, lstB):
    return lstA + lstB

