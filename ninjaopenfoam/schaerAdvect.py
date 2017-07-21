import os

from .case import Case
from .timing import Timing
from .solver import SolverExecution

class SchaerAdvect:
    def __init__(self, name, mesh, timestep, fvSchemes, parallel):
        self.case = Case(name)
        self.mesh = mesh
        self.timing = Timing(10000, 5000, timestep)
        self.fvSchemes = fvSchemes
        self.parallel = parallel

    def write(self, generator):
        g = generator
        case = self.case

        solver = SolverExecution(
                g,
                case,
                self.parallel,
                os.path.join("src", "schaerAdvect", "decomposeParDict.template")
        )
        solver.solve(
                outputs=[case.path(str(self.timing.endTime), "T"),
                         case.path(str(self.timing.writeInterval), "T")],
                rule="advectionFoam",
                implicit=[case.path("0", "T"), case.path("0", "phi")]
        )

        g.initialTracer(
                case,
                os.path.join("src", "schaerAdvect", "tracerField"),
                os.path.join("src", "schaerAdvect", "T_init")
        )

        g.w.build(
                outputs=case.path("0", "phi"),
                rule="setVelocityField",
                implicit=case.polyMesh + case.systemFiles + [case.velocityFieldDict],
                variables={"case": self.case}
        )
        g.w.newline()
        g.copy(os.path.join("src", "schaerAdvect", "velocityField"), case.velocityFieldDict)
        g.w.newline()

        g.copyMesh(source=self.mesh.case, target=case)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(os.path.join("src", "fvSolution"), case.fvSolution)
        g.controlDict(case, self.timing)

        g.s3upload(
                case,
                [case.path(str(self.timing.endTime), "T"),
                 case.path(str(self.timing.writeInterval), "T"),
                 case.path("0", "T")])

    def __str__(self):
        return self.case.name

