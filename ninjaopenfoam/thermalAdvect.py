from .advect import Advect
from .timing import Timing
from .sample import Sample

import os

class ThermalAdvect:
    def __init__(self, name, dx, mesh, timestep, fvSchemes,
            parallel, fast, fastMesh):
        if fast:
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')
            mesh = fastMesh
            timestep = 120

        tracerField = os.path.join('src/thermalAdvect/tracerField')
        velocityField = os.path.join('src/thermalAdvect/velocityField')
        T_init = os.path.join('src/schaerWaves/theta_init')

        self.timing = Timing(18000, 3600, timestep)
        self.sampleDict = os.path.join('src/thermalAdvect/sampleLine')

        self.advect = Advect(name, dx, 250, mesh,
                None, # TODO: staggering
                tracerField, velocityField,
                T_init, self.timing, fvSchemes, parallel, fast)

    def write(self, generator):
        self.advect.write(generator)

        endTime = str(self.timing.endTime)
        Sample(self.advect.case, endTime, 'T_diff', self.sampleDict).write(generator)

    def __str__(self):
        return str(self.advect)
