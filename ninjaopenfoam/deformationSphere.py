import collections
import os

from .case import Case
from .errors import Errors
from .paths import Paths
from .solver import SolverExecution
from .timing import Timing

class DeformationSphereBuilder:
    def __init__(self, parallel, fast):
        self.parallel = parallel
        self.fast = fast

    def collated(self, name, fvSchemes, tracerFieldDict, tests):
        tests = [self.test(t.name, t.mesh, t.timestep, fvSchemes, tracerFieldDict)
                for t in tests]
        return DeformationSphereCollated(name, tests, self.fast)

    def test(self, name, mesh, timestep, fvSchemes, tracerFieldDict):
        if self.fast:
            timestep = 6400
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return DeformationSphere(name, mesh, timestep, fvSchemes, tracerFieldDict, self.parallel)

class DeformationSphereCollated:
    Test = collections.namedtuple('DeformationSphereCollatedTest', ['name', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.fast = fast

    def write(self, generator):
        g = generator

        self.collateErrors(generator, 'l2errorT.txt')
        self.collateErrors(generator, 'linferrorT.txt')

    def collateErrors(self, generator, file):
        if self.fast:
            generator.w.build(
                    outputs=self.case.path('1036800', file),
                    rule='cp',
                    inputs=os.path.join('src/deformationSphere/collatedErrors.dummy'))
        else:
            generator.w.build(
                    outputs=self.case.path('1036800', file),
                    rule='collate',
                    implicit=[t.case.averageEquatorialSpacing for t in self.tests]
                            + [t.case.path('1036800', file) for t in self.tests],
                    variables={
                        "cases": [t.case.root for t in self.tests],
                        "independent": Paths.averageEquatorialSpacing,
                        "dependent": os.path.join('1036800', file)
                    }
            )

        generator.w.newline()
        
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

        self.lperrors(g)

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

    def lperrors(self, generator):
        endTime = str(self.timing.endTime)

        errors = Errors(self.case, endTime)
        errors.write(generator)

        generator.copy(self.case.path('0/T'), self.case.path(endTime, 'T_analytic'))

    def __str__(self):
        return self.case.name
