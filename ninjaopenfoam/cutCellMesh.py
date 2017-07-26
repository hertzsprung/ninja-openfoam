from .case import Case

import os

class CutCellMesh:
    def __init__(
            self,
            name,
            asamGridFile,
            createPatchDict,
            extrudeMeshDict=os.path.join('src/cutCellMesh/extrudeMeshDict'),
            meshQualityDict=os.path.join('src/cutCellMesh/meshQualityDict'),
            patchSets=os.path.join('src/cutCellMesh/patchSets')):
        self.case = Case(name)
        self.asamGridFile = asamGridFile
        self.createPatchDict = createPatchDict
        self.extrudeMeshDict = extrudeMeshDict
        self.meshQualityDict = meshQualityDict
        self.patchSets = patchSets

    def write(self, generator):
        g = generator
        case = self.case

#        g.w.build(
#                outputs=case.polyMesh,
#                rule="blockMesh",
#                inputs=case.blockMeshDict,
#                implicit=case.controlDict,
#                variables={"case": case}
#        )
        g.w.newline()

    def __str__(self):
        return self.case.name
