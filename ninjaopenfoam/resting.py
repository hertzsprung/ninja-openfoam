from .case import Case
from .collator import Collator
from .paths import Paths
from .solver import SolverExecution
from .timing import Timing

import collections
import os

class RestingBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collateByMountainHeight(self, name, fvSchemes, tests):
        tests = [self.test(t.name, t.mountainHeight, t.mesh, t.timestep, fvSchemes)
                for t in tests]
        return RestingCollated(name, tests, self.fast)

    def test(self, name, mountainHeight, mesh, timestep, fvSchemes):
        if self.fast:
            mesh = self.fastMesh
            timestep = 50
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return Resting(name, mountainHeight, mesh, 
                timestep, fvSchemes, self.parallel, self.fast)

class RestingCollated:
    Test = collections.namedtuple('RestingCollated', ['name', 'mountainHeight', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.mountainHeight, tests, fast,
                dummy=os.path.join('src/resting/collatedErrors.dummy'))

    def write(self, generator):
        self.collator.write(generator, Paths.maxw)
        self.collator.s3upload(generator, [Paths.maxw])

    def __str__(self):
        return self.case.name

class Resting:
    def __init__(self, name, mountainHeight, mesh, timestep, fvSchemes, parallel, fast):
        self.case = Case(name)
        self.mountainHeight = mountainHeight
        self.mesh = mesh
        if fast:
            self.timing = Timing(500, 500, timestep)
        else:
            self.timing = Timing(21600, 10800, timestep)
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

        g.w.build(
                outputs=case.maxw,
                rule='maxw',
                inputs=case.energy
        )
        g.w.newline()

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

        g.w.build(self.case.mountainHeight, 'echo', variables={'string': str(self.mountainHeight)})
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
            g.s3uploadCase(case, [case.maxw])

    def __str__(self):
        return self.case.name
