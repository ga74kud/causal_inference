import sympy
from sympy.utilities.lambdify import *
import causal_inference.util.data_input_loader as util_io

class scm_class(object):
    def __init__(self):
        None

    '''
        get the topology list from scm 
    '''
    def get_topology_by_scm(self, problem):
        scm=problem["scm"]
        dictionary=problem["variables"]
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

    '''
       get the problem with scm with a value list and get the expected values and variances
    '''
    def get_scm_function(self, problem, value_list):
        all_exp=[]
        all_var = []
        scms=list(problem["scm"].values())
        dictionary = problem["variables"]
        symb=sympy.symbols(list(dictionary.values()))
        scm_sympy = sympy.sympify(scms) #necessary for substitution later
        for idx, act_scm in enumerate(scm_sympy):
            expectation_scm, variance_scm=self.get_expected_val_scm(idx, act_scm, symb, value_list)
            all_exp.append(expectation_scm)
            all_var.append(variance_scm)
        return all_exp, all_var

    '''
        only the mean value function
    '''
    def get_scm_function_mean(self, problem, value_list):

        all_exp=[]
        scms=list(problem["scm"].values())
        dictionary = problem["variables"]
        param_dictionary = problem["parameters"]
        symb=sympy.symbols(list(dictionary.values()))
        param_symb = sympy.symbols(list(param_dictionary.values()))
        scm_sympy = sympy.sympify(scms) #necessary for substitution later
        for idx, act_scm in enumerate(scm_sympy):
            expectation_scm=self.get_expected_val_scm_mean(idx, act_scm, symb, value_list)
            expectation_scm=self.replace_param_value(idx, expectation_scm, param_symb)
            all_exp.append(expectation_scm)
        return all_exp

    '''
        Replace the variables for scm functions
    '''
    def replace_param_value(self, idx, expectation_scm, param_symb):
        params = util_io.get_params()
        Ts = params["general"]["Ts"]
        value_input=[Ts]
        a = sympy.symbols('a')
        new_fun = implemented_function("pr"+str(idx), lambda inp: expectation_scm.subs([(param_symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f = lambdify(a, new_fun(a))
        erg = lam_f(value_input)
        return erg

    '''
        get expected value for scm
    '''
    def get_expected_val_scm_mean(self, idx, act_scm, symb, value_input):
        from sympy.stats import E, variance
        a = sympy.symbols('a')
        new_fun=implemented_function('scm_'+str(idx), lambda inp: act_scm.subs([(symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f=lambdify(a, new_fun(a))
        erg=lam_f(value_input)
        return erg

    '''
        get expected value and variance of scm 
    '''
    def get_expected_val_scm(self, idx, act_scm, symb, probability_input):
        from sympy.stats import E, variance
        a = sympy.symbols('a')
        new_fun=implemented_function('scm_'+str(idx), lambda inp: act_scm.subs([(symb[i], inp[i]) for i in range(0, len(inp))]))
        lam_f=lambdify(a, new_fun(a))
        erg=lam_f(probability_input)
        E=E(erg)
        V=variance(erg)
        return E, V