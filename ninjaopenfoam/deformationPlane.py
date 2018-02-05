import collections
import os

from .case import Case
from .collator import Collator
from .paths import Paths

class DeformationPlaneBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, fvSchemes, tests,
            controlDict=Paths.defaultControlDict, solverRule=None):
        tests = [self.test(t.name, t.dx, t.mesh, t.timestep,
                        fvSchemes, controlDict, solverRule)
                for t in tests]
        return DeformationPlaneCollated(name, tests, self.fast)

    def test(self, name, dx, mesh, timestep,
            fvSchemes, controlDict, solverRule):
        if self.fast:
            mesh = self.fastMesh
            timestep = 0.004
            fvSchemes = os.path.join('src/deformationPlane/linearUpwind')
            controlDict = Paths.defaultControlDict
            solverRule = None

        return DeformationPlaneAdvect(name, dx, mesh, timestep,
                fvSchemes, self.parallel, self.fast, controlDict, solverRule)

class DeformationPlaneCollated:
    Test = collections.namedtuple('DeformationPlaneCollatedTest', ['name', 'dx', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.dx, tests, fast,
                dummy=os.path.join('src/deformationPlane/collatedErrors.dummy'))

    def write(self, generator):
        l2 = os.path.join('5/l2errorT.txt')
        linf = os.path.join('5/linferrorT.txt')

        self.collator.write(generator, l2)
        self.collator.write(generator, linf)
        self.collator.s3upload(generator, [l2, linf])
        
    def __str__(self):
        return self.case.name

class DeformationPlaneAdvect:
    def __init__(self, name, dx, mesh, timestep, fvSchemes, parallel, fast,
            controlDict, solverRule):
        self.case = Case(name)

    def write(self, generator):
        g = generator
        case = self.case

    def __str__(self):
        return self.case.name
