from causal_inference.src.uc_scm.manifold import *
from causal_inference.src.uc_scm.scm import *

class problem(object):
    def __init__(self, **kwargs):
        self.obj_manifold=None
        self.obj_solver=None

    def set_manifold(self):
        self.obj_manifold=manifold()

    def set_solver(self):
        self.obj_solver=scm_class()
        self.obj_solver.set_manifold(self.obj_manifold)
        self.obj_solver.scm_import_json()



if __name__ == '__main__':
    obj = problem()
    print(obj.obj_manifold.manifold)