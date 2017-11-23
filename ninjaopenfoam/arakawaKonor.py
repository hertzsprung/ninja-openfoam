from .case import Case
from .dynamics import DynamicsExecution
from .errors import Errors
from .staggering import CharneyPhillips, Lorenz
from .timing import Timing
from .thermalField import PerturbedThermalField

import os

class ArakawaKonor:
    lorenz = Lorenz(
            os.path.join('src/arakawaKonor/theta_init'),
            os.path.join('src/arakawaKonor/T_init'))

    charneyPhillips = CharneyPhillips(
            os.path.join('src/arakawaKonor/theta_init'),
            os.path.join('src/arakawaKonor/thetaf_init'),
            os.path.join('src/arakawaKonor/T_init'),
            os.path.join('src/arakawaKonor/Tf_init'))

    def __init__(self, name, mesh, staggering, fvSchemes, parallel, fast, fastMesh):
        self.case = Case(name)
        self.fast = fast

        if self.fast:
            mesh = fastMesh
            self.timing = Timing(172800, 43200, 400)
        else:
            self.timing = Timing(172800, 43200, 25)

        self.staggering = staggering

        thetaPerturbation = os.path.join('src/arakawaKonor/thetaPerturbation')
        self.dynamicsExecution = DynamicsExecution(
                self.case,
                mesh,
                self.timing,
                self.staggering,
                PerturbedThermalField(thetaPerturbation),
                os.path.join('src/arakawaKonor/Uf'),
                os.path.join('src/arakawaKonor/Exner_init'),
                os.path.join('src/arakawaKonor/environmentalProperties'),
                os.path.join('src/arakawaKonor/thermophysicalProperties'),
                fvSchemes,
                os.path.join('src/schaerWaves/fvSolution'),
                sponge=True,
                parallel=parallel)

    def write(self, generator):
        case = self.case
        g = generator
        endTime = str(self.timing.endTime)

        self.dynamicsExecution.write(generator)

        errors = Errors(case, endTime, 'theta')
        errors.diff(generator)

        g.copy(case.path('0/theta.background'), case.path(endTime, 'theta_analytic'))
        
        if not self.fast:
            g.s3uploadCase(
                    case,
                    [
                        case.path(endTime, 'theta_diff'),
                        case.path('0/theta_diff'),
                    ])

    def __str__(self):
        return self.case.name
