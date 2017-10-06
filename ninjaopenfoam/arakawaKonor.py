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

    def __init__(self, name, mesh, staggering, fvSchemes, parallel, fast, fastMesh):
        self.case = Case(name)
        if fast:
            mesh = fastMesh
            self.timing = Timing(172800, 43200, 400);
        else:
            self.timing = Timing(172800, 43200, 25);

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
        
#        if not self.fast:
#            g.s3uploadCase(
#                    case,
#                    [case.path(endTime, 'theta_diff')])

    def write(self, generator):
        case = self.case
        endTime = str(self.timing.endTime)

        self.dynamicsExecution.write(generator)

        errors = Errors(case, endTime, self.staggering.theta)
        errors.diff(generator)

        generator.copy(case.path('0/theta.background'), case.path(endTime, 'theta_analytic'))

    def __str__(self):
        return self.case.name
