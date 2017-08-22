import os

from .case import Case
from .sphericalMesh import SphericalMesh

class GeodesicHexMesh:
    def __init__(
            self,
            name,
            refinement,
            fast,
            extrudeMeshDict=os.path.join("src", "deformationSphere", "extrudeFromSurface"),
            fvSchemes=os.path.join("src", "fvSchemes"),
            fvSolution=os.path.join("src", "fvSolution"),
            controlDict=os.path.join("src", "controlDict")):
        self.case = Case(name)
        if fast:
            self.refinement = 3
        else:
            self.refinement = refinement
        self.extrudeMeshDict = extrudeMeshDict
        self.fvSchemes = fvSchemes
        self.fvSolution = fvSolution
        self.controlDict = controlDict

    def write(self, generator):
        g = generator
        case = self.case

        SphericalMesh(case).write(generator)

        g.w.build(
                outputs=case.polyMesh,
                rule="geodesicHexMesh",
                inputs=case.path("patch.obj"),
                implicit=[case.extrudeMeshDict] + case.systemFiles,
                variables={"case": case}
        )
        g.w.newline()

        g.w.build(
                outputs=case.path("patch.obj"),
                rule="geodesicHexPatch",
                variables={
                    "pool": "console",
                    "case": case,
                    "refinement": self.refinement
                }
        )
        g.w.newline()

        g.copy(self.extrudeMeshDict, case.extrudeMeshDict)
        g.copy(self.controlDict, case.controlDict)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)

    def __str__(self):
        return self.case.name
