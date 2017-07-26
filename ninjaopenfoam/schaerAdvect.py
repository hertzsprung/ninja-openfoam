import collections
import os

from .case import Case
from .errors import Errors
from .timing import Timing
from .solver import SolverExecution
from .paths import Paths

class SchaerAdvectBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, fvSchemes, tests):
        tests = [self.test(t.name, t.dx, t.mesh, t.timestep, fvSchemes)
                for t in tests]
        return SchaerAdvectCollated(name, tests, self.fast)

    def test(self, name, dx, mesh, timestep, fvSchemes):
        if self.fast:
            mesh = self.fastMesh
            timestep = 40
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return SchaerAdvect(name, dx, mesh, timestep, fvSchemes, self.parallel, self.fast)

class SchaerAdvectCollated:
    Test = collections.namedtuple('SchaerAdvectCollatedTest', ['name', 'dx', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.fast = fast

    def write(self, generator):
        g = generator

        self.collateErrors(generator, 'l2errorT.txt')
        self.collateErrors(generator, 'linferrorT.txt')

    def collateErrors(self, generator, file):
        endTime = '10000'

        if self.fast:
            generator.w.build(
                    outputs=self.case.path(endTime, file),
                    rule='cp',
                    inputs=os.path.join('src/schaerAdvect/collatedErrors.dummy'))
        else:
            generator.w.build(
                    outputs=self.case.path(endTime, file),
                    rule='collate',
                    implicit=[t.case.dx for t in self.tests]
                            + [t.case.path(endTime, file) for t in self.tests],
                    variables={
                        "cases": [t.case.root for t in self.tests],
                        "independent": Paths.dx,
                        "dependent": os.path.join(endTime, file)
                    }
            )

        generator.w.newline()
        
    def __str__(self):
        return self.case.name

class SchaerAdvect:
    def __init__(self, name, dx, mesh, timestep, fvSchemes, parallel, fast):
        self.case = Case(name)
        self.dx = dx
        self.mesh = mesh
        self.timing = Timing(10000, 5000, timestep)
        self.fvSchemes = fvSchemes
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
                os.path.join("src/schaerAdvect/decomposeParDict.template")
        )
        solver.solve(
                outputs=[case.path(str(self.timing.endTime), "T"),
                         case.path(str(self.timing.writeInterval), "T")],
                rule="advectionFoam",
                implicit=[case.path("0/T"), case.path("0/phi")]
        )

        g.initialTracer(
                case,
                os.path.join("src/schaerAdvect/tracerField"),
                os.path.join("src/schaerAdvect/T_init")
        )

        g.w.build(
                outputs=case.path("0/phi"),
                rule="setVelocityField",
                implicit=case.polyMesh + case.systemFiles + [case.velocityFieldDict],
                variables={"case": self.case}
        )
        g.w.newline()
        g.copy(os.path.join("src/schaerAdvect/velocityField"), case.velocityFieldDict)
        g.w.newline()

        g.copyMesh(source=self.mesh.case, target=case)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(os.path.join("src/fvSolution"), case.fvSolution)
        g.controlDict(case, self.timing)

        if not self.fast:
            g.s3upload(
                    case,
                    [case.path(str(self.timing.endTime), "T"),
                     case.path(str(self.timing.writeInterval), "T"),
                     case.path("0/T")])

    def lperrors(self, generator):
        g = generator
        case = self.case
        endTime = str(self.timing.endTime)

        errors = Errors(self.case, endTime)
        errors.write(g)

        g.w.build(
                self.case.path(endTime, 'T_analytic'),
                'setAnalyticTracerField',
                implicit=case.polyMesh + case.systemFiles + \
                        [case.velocityFieldDict, case.tracerFieldDict],
                variables={'case': case, 'time': endTime}
        )
        g.w.newline()

        g.w.build(
                self.case.dx,
                'echo',
                variables={'string': str(self.dx)}
        )
        g.w.newline()

    def __str__(self):
        return self.case.name

