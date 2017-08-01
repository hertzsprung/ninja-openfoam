from .case import Case
from .solver import SolverExecution
from .timing import Timing

import os

class Resting:
    def __init__(self, name, mesh, fvSchemes, parallel, fast):
        self.case = Case(name)
        self.mesh = mesh
        if fast:
            self.timing = Timing(500, 500, 25)
        else:
            self.timing = Timing(21600, 10800, 25)
        self.initialUf = os.path.join('src/resting/Uf')
        self.thetaInit = os.path.join('src/resting/theta_init')
        self.exnerInit = os.path.join('src/resting/Exner_init')
        self.environmentalProperties = os.path.join('src/resting/environmentalProperties')
        self.thermophysicalProperties = os.path.join('src/resting/thermophysicalProperties')
        self.fvSchemes = fvSchemes
        self.fvSolution = os.path.join('src/resting/fvSolution')
        self.parallel = parallel
        self.fast = fast

    def write(self, generator):
        g = generator
        case = self.case

        solver = SolverExecution(
                g,
                case,
                self.parallel,
                os.path.join("src/advect/decomposeParDict.template")
        )
        solver.solve(
                outputs=case.energy,
                rule='exnerFoamH',
                implicit=case.polyMesh + case.systemFiles + [
                    case.path('0/Uf'),
                    case.path('0/theta'),
                    case.path('0/Exner'),
                    case.environmentalProperties,
                    case.thermophysicalProperties
                ]
        )

        g.w.build(
                outputs=case.path('0/theta'),
                rule='setTheta',
                implicit=case.polyMesh + case.systemFiles + [
                    case.thetaInit,
                    case.environmentalProperties,
                    case.thermophysicalProperties
                ],
                variables={'case': case}
        )
        g.w.newline()

        g.w.build(
                outputs=case.path('0/Exner'),
                rule='setExnerBalancedH',
                implicit=case.polyMesh + case.systemFiles + [
                    case.exnerInit,
                    case.path('0/theta'),
                    case.environmentalProperties,
                    case.thermophysicalProperties
                ],
                variables={'case': case}
        )
        g.w.newline()

#        g.w.build(
#                outputs=case.sponge,
#                rule='createSpongeLayer',
#                implicit=case.polyMesh + case.systemFiles + \
#                    [case.environmentalProperties],
#                variables={'case': case}
#        )
#        g.w.newline()

        g.copyMesh(source=self.mesh.case, target=case)
        g.copy(self.initialUf, case.path('0/Uf'))
        g.copy(self.thetaInit, case.thetaInit)
        g.copy(self.exnerInit, case.exnerInit)
        g.copy(self.environmentalProperties, case.environmentalProperties)
        g.copy(self.thermophysicalProperties, case.thermophysicalProperties)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.controlDict(case, self.timing)

        if not self.fast:
            g.s3upload(case, [case.energy])

    def __str__(self):
        return self.case.name
