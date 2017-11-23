import collections
import os

from .case import Case
from .collator import Collator
from .errors import Errors
from .paths import Paths
from .solver import SolverExecution
from .staggering import Lorenz
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

        return DeformationSphere(name, mesh, timestep, fvSchemes, tracerFieldDict, self.parallel, self.fast)

class DeformationSphereCollated:
    Test = collections.namedtuple('DeformationSphereCollatedTest', ['name', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.averageEquatorialSpacing, tests, fast,
                dummy=os.path.join('src/deformationSphere/collatedErrors.dummy'))

    def write(self, generator):
        l2 = os.path.join('1036800/l2errorT.txt')
        linf = os.path.join('1036800/linferrorT.txt')

        self.collator.write(generator, l2)
        self.collator.write(generator, linf)
        self.collator.s3upload(generator, [l2, linf])
        
    def __str__(self):
        return self.case.name

class DeformationSphere:
    def __init__(self, name, mesh, timestep, fvSchemes, tracerFieldDict, parallel, fast):
        self.case = Case(name)
        self.mesh = mesh
        self.timing = Timing(1036800, 172800, timestep)
        self.fvSchemes = fvSchemes
        self.tracerFieldDict = tracerFieldDict
        self.parallel = parallel
        self.fast = fast

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
                Lorenz.advect(os.path.join("src/deformationSphere/T_init"))
        )

        g.copy(os.path.join("src/deformationSphere/nonDivergent"), case.advectionDict)
        g.copyMesh(source=self.mesh.case, target=case)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(os.path.join("src", "fvSolution"), case.fvSolution)
        g.copy(self.mesh.case.averageEquatorialSpacing, case.averageEquatorialSpacing)
        g.controlDict(case, self.timing)

        if not self.fast:
            g.s3uploadCase(
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
