from .case import Case
from .errors import Errors
from .dynamics import DynamicsExecution
from .sample import Sample
from .staggering import CharneyPhillips, Lorenz
from .timing import Timing
from .thermalField import StratifiedThermalField

import os

class SchaerWaves:
    charneyPhillips = CharneyPhillips(
            os.path.join('src/schaerWaves/theta_init'),
            os.path.join('src/schaerWavesCP/thetaf_init'))
    lorenz = Lorenz.dynamics(os.path.join('src/schaerWaves/theta_init'))

    def __init__(self, name, mesh, timestep, staggering, fvSchemes, parallel, fast, fastMesh):
        self.case = Case(name)
        self.fast = fast

        if self.fast:
            fvSchemes = os.path.join('src/schaerWaves/linearUpwindFast')
            mesh = fastMesh
            timestep = 120

        self.timing = Timing(18000, 3600, timestep)
        self.staggering = staggering
        self.sampleDict = os.path.join('src/schaerWaves/sampleLine')

        self.dynamicsExecution = DynamicsExecution(
                self.case,
                mesh,
                self.timing,
                self.staggering,
                StratifiedThermalField(),
                os.path.join('src/schaerWaves/Uf'),
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
        staggering = self.staggering
        endTime = str(self.timing.endTime)

        self.dynamicsExecution.write(generator)

        errors = Errors(self.case, self.timing.endTime, 'theta')
        errors.diff(generator)

        Sample(self.case, endTime, 'theta_diff', self.sampleDict).write(generator)

        generator.copy(self.case.path('0/theta'), self.case.path(endTime, 'theta_analytic'))
        
        if not self.fast:
            g.s3uploadCase(
                    case,
                    [case.path(endTime, 'theta_diff')])

    def __str__(self):
        return self.case.name
