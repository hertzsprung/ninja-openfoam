import collections
import os

from .case import Case
from .paths import Paths
from .solver import SolverExecution
from .timing import Timing

class DeformationSphereBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, fvSchemes, tracerFieldDict, tests):
        tests = [self.test(t.name, t.mesh, t.timestep, fvSchemes, tracerFieldDict)
                for t in tests]
        return DeformationSphereCollated(name, tests)

    def test(self, name, mesh, timestep, fvSchemes, tracerFieldDict):
        if self.fast:
            mesh = self.fastMesh
            timestep = 6400
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return DeformationSphere(name, mesh, timestep, fvSchemes, tracerFieldDict, self.parallel)

class DeformationSphereCollated:
    Test = collections.namedtuple('DeformationSphereCollatedTest', ['name', 'mesh', 'timestep'])

    def __init__(self, name, tests):
        self.case = Case(name)
        self.tests = tests

    def write(self, generator):
        g = generator

        g.w.build(
                outputs=self.case.path('1036800/l2errorT.txt'),
                rule='collate',
                implicit=[t.case.averageEquatorialSpacing for t in self.tests]
                        + [t.case.path('1036800/l2errorT.txt') for t in self.tests],
                variables={
                    "cases": [t.case.root for t in self.tests],
                    "independent": Paths.averageEquatorialSpacing,
                    "dependent": '1036800/l2errorT.txt'
                }
        )
        g.w.newline()

        for t in self.tests:
            t.write(g)
        
    def __str__(self):
        return self.case.name

class DeformationSphere:
    def __init__(self, name, mesh, timestep, fvSchemes, tracerFieldDict, parallel):
        self.case = Case(name)
        self.mesh = mesh
        self.timing = Timing(1036800, 172800, timestep)
        self.fvSchemes = fvSchemes
        self.tracerFieldDict = tracerFieldDict
        self.parallel = parallel

    def write(self, generator):
        g = generator
        case = self.case

        self.l2error(g)

        solver = SolverExecution(
                g,
                case,
                self.parallel,
                os.path.join("src/deformationSphere/decomposeParDict.template")
        )
        solver.solve(
                outputs=[case.path(str(self.timing.endTime), "T"),
                         case.path(str(self.timing.endTime//2), "T")],
                rule="sphericalAdvectionFoam",
                implicit=[case.path("0", "T"), case.advectionDict]
        )

        g.initialTracer(
                case,
                self.tracerFieldDict,
                os.path.join("src/deformationSphere/T_init")
        )

        g.copy(os.path.join("src/deformationSphere/nonDivergent"), case.advectionDict)
        g.copyMesh(source=self.mesh.case, target=case)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(os.path.join("src", "fvSolution"), case.fvSolution)
        g.copy(self.mesh.case.averageEquatorialSpacing, case.averageEquatorialSpacing)
        g.controlDict(case, self.timing)

        g.s3upload(
                case,
                [case.path(str(self.timing.endTime), "T"),
                 case.path(str(self.timing.endTime//2), "T"),
                 case.path("0", "T")])

    def l2error(self, generator):
        g = generator
        case = self.case
        endTime = str(self.timing.endTime)

        g.l2error(case, endTime)
        g.diff(case, endTime)
        g.copy(case.path('0/T'), case.path(endTime, 'T_analytic'))

    def __str__(self):
        return self.case.name
