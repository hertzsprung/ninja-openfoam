from .advect import Advect
from .case import Case
from .timing import Timing

import os

class ArakawaKonorAdvect:
    def __init__(self, name, mesh, staggering, fvSchemes, parallel, fast, fastMesh):
        self.case = Case(name)
        self.fast = fast

        if self.fast:
            mesh = fastMesh
            self.timing = Timing(60000, 30000, 400)
        else:
            self.timing = Timing(60000, 30000, 25)

        self.staggering = staggering

        tracerFieldDict = os.path.join('src/arakawaKonorAdvect/tracerFieldDict')
        velocityFieldDict = os.path.join('src/arakawaKonorAdvect/velocityFieldDict')
        T_init = os.path.join('src/arakawaKonorAdvect/T_init')

        self.advect = Advect(name, 0, 0, mesh, 
            tracerFieldDict, velocityFieldDict, T_init, self.timing,
            fvSchemes, parallel, fast)

    def write(self, generator):
        self.advect.write(generator)

    def __str__(self):
        return self.case.name
