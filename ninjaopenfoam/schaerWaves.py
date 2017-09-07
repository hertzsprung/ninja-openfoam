from .case import Case
from .errors import Errors
from .dynamics import DynamicsExecution
from .timing import Timing

import os

class SchaerWaves:
    def __init__(self, name, mesh, timestep, fvSchemes, parallel, fast, fastMesh):
        self.case = Case(name)

        if fast:
            fvSchemes = os.path.join('src/schaerWaves/linearUpwind')
            mesh = fastMesh
            timestep = 120

        self.timing = Timing(18000, 3600, timestep)

        self.dynamicsExecution = DynamicsExecution(
                self.case,
                mesh,
                self.timing,
                os.path.join('src/schaerWaves/Uf'),
                os.path.join('src/schaerWaves/theta_init'),
                os.path.join('src/schaerWaves/Exner_init'),
                os.path.join('src/schaerWaves/environmentalProperties'),
                os.path.join('src/schaerWaves/thermophysicalProperties'),
                fvSchemes,
                os.path.join('src/schaerWaves/fvSolution'),
                sponge=True,
                parallel=parallel)

    def write(self, generator):
        g = generator
        case = self.case
        endTime = str(self.timing.endTime)

        self.dynamicsExecution.write(generator)

        errors = Errors(self.case, self.timing.endTime, 'theta')
        errors.diff(generator)

        generator.copy(self.case.path('0/theta'), self.case.path(endTime, 'theta_analytic'))
        
        # TODO: s3upload

    def __str__(self):
        return self.case.name
