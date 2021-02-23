import causal_inference as ci
problem = {'variables': {'000': 'A', '001': 'B', '002': 'C', '003': 'D'},
               'scm': {'000': 'A*x+B*y', '001': 'C*x+D*y'}}
input=[[1, .1], [2, 0.1], [3, 0.1], [4, 0.1]]
all_exp, all_var = ci.get_scm_solution(problem, input)
print(all_exp)
print(all_var)
