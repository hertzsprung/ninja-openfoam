from .case import Case

import os

class SlantedCellMesh:
    def __init__(
            self,
            name,
            blockMesh,
            mountainDict,
            collapseDict=os.path.join('src/slantedCellMesh/collapseDict'),
            meshQualityDict=os.path.join('src/mesh/meshQualityDict'),
            removeTinyCells=os.path.join('src/slantedCellMesh/removeTinyCells'),
            fvSchemes=os.path.join('src/fvSchemes'),
            fvSolution=os.path.join('src/fvSolution'),
            controlDict=os.path.join('src/controlDict')):
        self.case = Case(name)
        self.blockMesh = blockMesh
        self.mountainDict = mountainDict
        self.collapseDict = collapseDict
        self.meshQualityDict = meshQualityDict
        self.removeTinyCells = removeTinyCells
        self.fvSchemes = fvSchemes
        self.fvSolution = fvSolution
        self.controlDict = controlDict

    def write(self, generator):
        g = generator
        case = self.case
        blockMesh = self.blockMesh

        g.w.build(
                outputs=case.polyMesh,
                rule='slantedCellMesh',
                inputs=case.mountainDict,
                implicit=blockMesh.case.polyMesh
                        + case.systemFiles
                        + [
                            case.collapseDict,
                            case.meshQualityDict,
                            self.removeTinyCells
                          ],
                variables={
                    'blockMeshCase': blockMesh.case,
                    'slantedCellMeshCase': case,
                    'removeTinyCells': self.removeTinyCells
                }
        )
        g.w.newline()

        g.copy(self.mountainDict, case.mountainDict)
        g.copy(self.collapseDict, case.collapseDict)
        g.copy(self.meshQualityDict, case.meshQualityDict)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.copy(self.controlDict, case.controlDict)

    def __str__(self):
        return self.case.name

