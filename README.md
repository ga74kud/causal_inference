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
import numpy as np
probs={'A': [1, 0.1], 'B': [1, 0.1], 'C': [1, 0.1], 'D': [1, 0.1]}
xy={"mean": np.array([[1, 2], [2, 4]]), "dev": np.array([[.1, .2], [.2, .4]])}

new_xv=ci.next_position_scm(xy, probs)
print(new_xv["mean"])
print(new_xv["dev"])
```




# Citation

Please cite following document if you use this python package:
```
TBD
```


Image source: https://www.pexels.com/photo/blue-water-2695624/