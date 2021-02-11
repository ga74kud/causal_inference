import sympy
from sympy.stats import Normal
from sympy.utilities.lambdify import *
import causal_inference.util.data_input_loader as util_io

class scm_class(object):
    def __init__(self):
        None

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
        get expected value and variance of scm 
    '''
    def get_expected_val_scm(self, idx, act_scm, symb, input_values):
        from sympy.stats import E, variance
        a = sympy.symbols('a')
        new_fun=implemented_function('scm_'+str(idx), lambda inp: act_scm.subs((symb[i], Normal(symb[i], inp[i][0], inp[i][1])) for i in range(0, len(inp))))
        lam_f=lambdify(a, new_fun(a))
        erg=lam_f(input_values)
        E=E(erg)
        V=variance(erg)
        return E, V