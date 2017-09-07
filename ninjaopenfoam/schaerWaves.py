from .case import Case
from .dynamics import DynamicsExecution
from .timing import Timing

import os

class SchaerWaves:
    def __init__(self, name, mesh, timestep, fvSchemes, parallel, fast):
        self.case = Case(name)

        if fast:
            fvSchemes = os.path.join('src/schaerWaves/linearUpwind')
            # TODO: fastMesh?

        self.dynamicsExecution = DynamicsExecution(
                self.case,
                mesh,
                Timing(18000, 3600, timestep),
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

        self.dynamicsExecution.write(generator)
        
        # TODO: theta_diff
        # TODO: s3upload

    def __str__(self):
        return self.case.name
