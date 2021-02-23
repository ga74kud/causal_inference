![](/images/pexels_splash.jpg)


# Causal Inference

- [ ] Causal Inference

# Installation
```bash
pip install causal-inference
```

# Usage

```python
import causal_inference as ci
problem = {'variables': {'000': 'V', '001': 'F'},
               'scm': {'000': 'V', '001': '2*V+F'}}
input=[[1, .1], [2, 0.1]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           ]
all_exp, all_var = ci.get_scm_solution(problem, input)
```




# Citation

Please cite following document if you use this python package:
```
TBD
```


Image source: https://www.pexels.com/photo/blue-water-2695624/