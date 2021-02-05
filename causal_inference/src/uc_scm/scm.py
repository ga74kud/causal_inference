import igraph as ig
import sympy
from sympy.utilities.lambdify import *
import json
import numpy as np
import causal_inference.util.data_input_loader as util_io

class scm_class(object):
    def __init__(self):
        self.manifold=None
        self.data=None
    def set_manifold(self, manifold):
        self.manifold=manifold.manifold

    def set_adjacency_list(self, nodes, list):
        new_list = []
        for i in list:
            a = nodes.index(i[0])
            b = nodes.index(i[1])
            new_list.append((a, b))
        return new_list
    def scm_import_json(self):
        f = open('scm_v1.json', "r")
        self.data = json.loads(f.read())
        self.manifold['amount_states'] = len(self.data['scm'])
        self.manifold['X'] = [qrt for qrt in self.data['variables']]
        self.manifold['Topology']=self.get_topology_by_scm(self.data)

        #self.get_adjacency(self.manifold['amount_states'])
        #self.set_neighbour_actions()
    def get_topology_by_scm(self, data):
        scm=data["scm"]
        dictionary=data["variables"]
        list_values=list(dictionary.values())
        abc_keys = list(dictionary.keys())
        abc = list(scm.values())
        topology=[]
        for idx, qrt in enumerate(list_values):
            for idx2, qrt2 in enumerate(abc):
                check_val=qrt
                check_str=qrt2.find(check_val)
                if (check_str != -1):
                    topology.append([abc_keys[idx], abc_keys[idx2]])
        return topology

    def get_scm_function(self, input, probability_input):
        all_exp=[]
        all_var = []
        scms=list(input["scm"].values())
        dictionary = input["variables"]
        symb=sympy.symbols(list(dictionary.values()))
        scm_sympy = sympy.sympify(scms) #necessary for substitution later
        for idx, act_scm in enumerate(scm_sympy):
            expectation_scm, variance_scm=self.get_expected_val_scm(idx, act_scm, symb, probability_input)
            #print(expectation_scm)
            all_exp.append(expectation_scm)
            all_var.append(variance_scm)
        return all_exp, all_var

    '''
    mean_input is the 
    '''
    def get_scm_function_mean(self, input, mean_input):

        all_exp=[]
        scms=list(input["scm"].values())
        dictionary = input["variables"]
        param_dictionary = input["parameters"]
        symb=sympy.symbols(list(dictionary.values()))
        param_symb = sympy.symbols(list(param_dictionary.values()))
        scm_sympy = sympy.sympify(scms) #necessary for substitution later
        for idx, act_scm in enumerate(scm_sympy):
            expectation_scm=self.get_expected_val_scm_mean(idx, act_scm, symb, mean_input)
            expectation_scm=self.replace_param_value(idx, expectation_scm, param_symb)
            all_exp.append(expectation_scm)
        return all_exp
    def replace_param_value(self, idx, expectation_scm, param_symb):
        params = util_io.get_params()
        Ts = params["general"]["Ts"]
        value_input=[Ts]
        a = sympy.symbols('a')
        new_fun = implemented_function("pr"+str(idx), lambda inp: expectation_scm.subs([(param_symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f = lambdify(a, new_fun(a))
        erg = lam_f(value_input)
        return erg

    def get_expected_val_scm_mean(self, idx, act_scm, symb, value_input):
        from sympy.stats import E, variance
        a = sympy.symbols('a')
        new_fun=implemented_function('scm_'+str(idx), lambda inp: act_scm.subs([(symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f=lambdify(a, new_fun(a))
        erg=lam_f(value_input)
        return erg
    def get_expected_val_scm(self, idx, act_scm, symb, probability_input):
        from sympy.stats import E, variance
        a = sympy.symbols('a')
        new_fun=implemented_function('scm_'+str(idx), lambda inp: act_scm.subs([(symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f=lambdify(a, new_fun(a))
        erg=lam_f(probability_input)
        E=E(erg)
        V=variance(erg)
        return E, V
    def set_neighbour_actions(self):
        for wlt in range(0, np.size(self.manifold['Adjacency'], 1)):
            abc=self.manifold['Adjacency'][:, wlt]
            all_actions=[self.manifold['X'][idx] for idx, qrt in enumerate(abc) if abc[idx] == True]
            self.manifold['Actions'].update({self.manifold['X'][wlt]: all_actions})
    def get_adjacency(self, am_nodes):
        self.manifold['Adjacency']=np.eye(am_nodes, dtype=bool)
        for wlt in self.manifold['Topology']:
            self.manifold['Adjacency'][int(wlt[1])][int(wlt[0])] = True
        test_symmetry=np.allclose(self.manifold['Adjacency'], self.manifold['Adjacency'].T, rtol=1e-05, atol=1e-08)
        print('symmetry')
        print(test_symmetry)

    def visualize_network(self):
        nodes=self.manifold['X']
        nodes_name=[self.data['variables'][i] for i in nodes]
        adjacency=self.set_adjacency_list(nodes, self.manifold['Topology'])
        g = ig.Graph(adjacency, directed=True)
        g.vs["name"] = nodes_name
        g.vs["label"] = g.vs["name"]
        g.vs["vertex_size"] = 20
        visual_style = {}
        visual_style["edge_curved"] = False
        ig.plot(g, **visual_style)#margin = 20,bbox = (3000, 3000), layout=layout,


