from .case import Case
from .paths import Paths
from .errors import Errors
from .solver import SolverExecution
from .timing import Timing

import os

class Advect:
    def __init__(self, name, dx, mountainHeight, mesh, staggering,
            tracerFieldDict, velocityFieldDict, timing,
            fvSchemes, parallel, fast, controlDict=Paths.defaultControlDict):
        self.case = Case(name)
        self.dx = dx
        self.mountainHeight = mountainHeight
        self.mesh = mesh
        self.staggering = staggering
        self.tracerFieldDict = tracerFieldDict
        self.velocityFieldDict = velocityFieldDict
        self.timing = timing
        self.fvSchemes = fvSchemes
        self.fvSolution = os.path.join('src/fvSolution')
        self.controlDict = controlDict
        self.parallel = parallel
        self.fast = fast

        self.solverDependencies = [
                self.case.path('0', staggering.T),
                self.case.path('0/phi')] + \
                self.staggering.advectionSolverDependencies(self.case)

    def addSolverDependency(self, dependency):
        self.solverDependencies += dependency

    def write(self, generator):
        g = generator
        case = self.case
        staggering = self.staggering

        self.lperrors(g)

        solver = SolverExecution(
                g,
                case,
                self.parallel,
                os.path.join("src/advect/decomposeParDict.template")
        )
        solver.solve(
                outputs=[
                    case.path(str(self.timing.endTime), staggering.T),
                    case.energy
                ],
                rule=staggering.advectionSolverRule,
                implicit=self.solverDependencies
        )
        staggering.copyAdvectionSolverDependencies(g, case)

        g.initialTracer(
                case,
                self.tracerFieldDict,
                staggering
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
        g.controlDict(case, self.timing, self.controlDict)

        if not self.fast:
            g.s3uploadCase(
                    case,
                    [case.path(str(self.timing.endTime), "T"),
                     case.path("0/T")])

    def lperrors(self, generator):
        g = generator
        case = self.case
        endTime = str(self.timing.endTime)
        staggering = self.staggering

        errors = Errors(self.case, endTime, staggering.T)
        errors.write(g)

        g.w.build(
                self.case.path(endTime, staggering.T_analytic),
                'setAnalyticTracerField',
                implicit=case.polyMesh + case.systemFiles + \
                [
                    case.velocityFieldDict,
                    case.tracerFieldDict,
                    case.T_init
                ],
                variables={'case': case, 'time': endTime}
        )
        g.w.newline()

    def __str__(self):
        return self.case.name

