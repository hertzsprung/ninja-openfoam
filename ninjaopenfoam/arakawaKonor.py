from .case import Case
from .dynamics import DynamicsExecution
from .staggering import CharneyPhillips, Lorenz
from .timing import Timing

import os

class ArakawaKonor:
    lorenz = Lorenz(os.path.join('src/arakawaKonor/theta_init'))

    def __init__(self, name, mesh, staggering, fvSchemes, parallel, fast):
        self.case = Case(name)
        timing = Timing(172800, 43200, 25);

        self.dynamicsExecution = DynamicsExecution(
                self.case,
                mesh,
                timing,
                staggering,
                os.path.join('src/arakawaKonor/Uf'),
                os.path.join('src/arakawaKonor/Exner_init'),
                os.path.join('src/arakawaKonor/environmentalProperties'),
                os.path.join('src/arakawaKonor/thermophysicalProperties'),
                fvSchemes,
                os.path.join('src/schaerWaves/fvSolution'),
                sponge=True,
                parallel=parallel)

    def write(self, generator):
        self.dynamicsExecution.write(generator)

    def __str__(self):
        return self.case.name
