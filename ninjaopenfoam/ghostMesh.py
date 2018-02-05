import os

from .case import Case
from .paths import Paths

class GhostMesh:
    def __init__(self, name, blockMeshDict,
            fvSchemesPrimary=os.path.join('src/ghostMesh/fvSchemes.primary'),
            fvSchemesGhost=os.path.join('src/ghostMesh/fvSchemes.ghost'),
            fvSolution=os.path.join('src/fvSolution'),
            controlDict=os.path.join('src/controlDict')):
        self.case = Case(name)
        self.blockMeshDict = blockMeshDict
        self.fvSchemesPrimary = fvSchemesPrimary
        self.fvSchemesGhost = fvSchemesGhost
        self.fvSolution = fvSolution
        self.controlDict = controlDict

    def write(self, generator):
        g = generator
        case = self.case

        g.w.build(
                outputs=case.polyMesh + case.ghostPolyMesh,
                rule="ghostMesh",
                inputs=case.blockMeshDict,
                implicit=[
                    case.fvSchemes,
                    case.fvSolution,
                    case.path('system/ghostMesh/fvSchemes'),
                    case.path('system/ghostMesh/fvSolution'),
                    case.controlDict],
                variables={"case": case}
        )
        g.w.newline()

        g.copy(self.blockMeshDict, case.blockMeshDict)
        g.copy(self.fvSchemesPrimary, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.copy(self.fvSchemesGhost, case.path('system/ghostMesh/fvSchemes'))
        g.copy(self.fvSolution, case.path('system/ghostMesh/fvSolution'))
        g.copy(self.controlDict, case.controlDict)

    def __str__(self):
        return self.case.name


