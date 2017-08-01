from .case import Case
from .errors import Errors
from .solver import SolverExecution
from .timing import Timing

import os

class Advect:
    def __init__(self, name, dx, mountainHeight, mesh, 
            tracerFieldDict, velocityFieldDict, timestep, fvSchemes, parallel, fast):
        self.case = Case(name)
        self.dx = dx
        self.mountainHeight = mountainHeight
        self.mesh = mesh
        self.tracerFieldDict = tracerFieldDict
        self.velocityFieldDict = velocityFieldDict
        self.timing = Timing(10000, 5000, timestep)
        self.fvSchemes = fvSchemes
        self.fvSolution = os.path.join('src/fvSolution')
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
                os.path.join("src/advect/decomposeParDict.template")
        )
        solver.solve(
                outputs=[case.path(str(self.timing.endTime), "T")],
                rule="advectionFoam",
                implicit=[case.path("0/T"), case.path("0/phi")]
        )

        g.initialTracer(
                case,
                self.tracerFieldDict,
                os.path.join("src/schaerAdvect/T_init")
        )

        g.w.build(
                outputs=case.path("0/phi"),
                rule="setVelocityField",
                implicit=case.polyMesh + case.systemFiles + [case.velocityFieldDict],
                variables={"case": self.case}
        )
        g.w.newline()

        g.w.build(
                outputs=case.courantNumber,
                rule='courantNumber',
                implicit=case.polyMesh + case.systemFiles + [case.path('0/phi')],
                variables={'case': self.case}
        )
        g.w.newline()

        g.w.build(self.case.dx, 'echo', variables={'string': str(self.dx)})
        g.w.build(self.case.mountainHeight, 'echo', variables={'string': str(self.mountainHeight)})
        g.w.build(self.case.timestep, 'echo', variables={'string': str(self.timing.timestep)})

        g.copyMesh(source=self.mesh.case, target=case)
        g.copy(self.velocityFieldDict, case.velocityFieldDict)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.controlDict(case, self.timing)

        if not self.fast:
            g.s3uploadCase(
                    case,
                    [case.path(str(self.timing.endTime), "T"),
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

    def __str__(self):
        return self.case.name

