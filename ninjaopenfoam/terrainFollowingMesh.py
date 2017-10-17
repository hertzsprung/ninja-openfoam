import os

from .case import Case

class TerrainFollowingMesh:
    def __init__(self, name, blockMesh, mountainDict,
            fvSchemes=os.path.join('src/fvSchemes'),
            fvSolution=os.path.join('src/fvSolution'),
            controlDict=os.path.join("src", "controlDict")):
        self.case = Case(name)
        self.blockMesh = blockMesh
        self.mountainDict = mountainDict
        self.fvSchemes = fvSchemes
        self.fvSolution = fvSolution
        self.controlDict = controlDict

    def write(self, generator):
        g = generator
        case = self.case

        g.w.build(
                outputs=case.polyMesh,
                rule="terrainFollowingMesh",
                inputs=case.mountainDict,
                implicit=self.blockMesh.case.polyMesh + [case.controlDict],
                variables={
                    "blockMeshCase": self.blockMesh.case,
                    "terrainFollowingMeshCase": case
                }
        )
        g.w.newline()

        g.copy(self.mountainDict, case.mountainDict)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.copy(self.controlDict, case.controlDict)

        g.s3uploadCase(case, case.polyMesh)

    def __str__(self):
        return self.case.name
