import os

from .blockMesh import BlockMesh
from .case import Case

class CubedSphereMesh:
    def __init__(
            self,
            name,
            nxPerPatch,
            fast,
            extrudeMeshDict=os.path.join("src", "deformationSphere", "extrudeFromPatch"),
            fvSchemes=os.path.join("src", "fvSchemes"),
            fvSolution=os.path.join("src", "fvSolution"),
            controlDict=os.path.join("src", "controlDict")):
        self.case = Case(name)
        self.blockMesh = BlockMesh(name + '-block', self.case.blockMeshDict)
        self.nxPerPatch = nxPerPatch
        self.fvSchemes = fvSchemes
        self.fvSolution = fvSolution
        self.controlDict = controlDict

    def write(self, generator):
        g = generator
        case = self.case
        blockMesh = self.blockMesh

        blockMesh.write(generator)

        g.w.build(
                case.blockMeshDict,
                'gen-cubedSphere-blockMeshDict',
                os.path.join('src/deformationSphere/cubedSphere.blockMeshDict.template'),
                variables={'nxPerPatch': self.nxPerPatch}
        )
        g.w.newline()

        g.w.build(
                case.extrudeMeshDict,
                'gen-cubedSphere-extrudeMeshDict',
                os.path.join('src/deformationSphere/extrudeFromPatch'),
                variables={'blockMeshCase': blockMesh.case}
        )
        g.w.newline()

        g.w.build(
                case.polyMesh,
                'cubedSphereMesh',
                implicit=[case.extrudeMeshDict, case.controlDict, case.fvSchemes] 
                        + blockMesh.case.polyMesh
                        + blockMesh.case.systemFiles,
                variables={'case': case, 'blockMeshCase': blockMesh.case}
        )
        g.w.newline()

        g.copy(self.fvSchemes, blockMesh.case.fvSchemes)
        g.copy(self.fvSolution, blockMesh.case.fvSolution)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.controlDict, case.controlDict)

    def __str__(self):
        return self.case.name
