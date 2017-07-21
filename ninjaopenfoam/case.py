from .paths import Paths

import os

class Case:
    def __init__(self, name, prefix='$builddir'):
        self.name = name
        self.root = os.path.join(prefix, name)
        self.advectionDict = self.path("system", "advectionDict")
        self.blockMeshDict = self.path("system", "blockMeshDict")
        self.controlDict = self.path("system", "controlDict")
        self.decomposeParDict = self.path("system", "decomposeParDict")
        self.extrudeMeshDict = self.path("system", "extrudeMeshDict")
        self.fvSchemes = self.path("system", "fvSchemes")
        self.fvSolution = self.path("system", "fvSolution")
        self.mountainDict = self.path("system", "mountainDict")
        self.T_init = self.path("constant", "T_init")
        self.tracerFieldDict = self.path("system", "tracerFieldDict")
        self.velocityFieldDict = self.path("system", "velocityFieldDict")

        self.polyMesh = [self.path(f) for f in Paths.polyMesh]
        self.systemFiles = [self.fvSchemes, self.fvSolution, self.controlDict]

    def path(self, path, *paths):
        return os.path.join(self.root, path, *paths)

    def __str__(self):
        return self.root

