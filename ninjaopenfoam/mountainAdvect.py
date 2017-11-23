import collections
import os

from .advect import Advect
from .case import Case
from .collator import Collator
from .paths import Paths
from .timing import Timing

class MountainAdvectBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collateByMountainHeight(self, name, dx, fvSchemes, tests):
        tests = [self.test(t.name, dx, t.mountainHeight, t.mesh, t.velocityField, t.timestep, fvSchemes)
                for t in tests]
        return MountainAdvectCollatedByMountainHeight(name, tests, self.fast)

    def collateByMeshSpacing(self, name, mountainHeight, velocityField, fvSchemes, tests):
        tests = [self.test(t.name, t.dx, mountainHeight, t.mesh, velocityField, t.timestep, fvSchemes)
                for t in tests]
        return MountainAdvectCollatedByMeshSpacing(name, tests, self.fast)

    def test(self, name, dx, mountainHeight, mesh, velocityField, timestep, fvSchemes):
        if self.fast:
            mesh = self.fastMesh
            timestep = 40
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return Advect(name, dx, mountainHeight, mesh,
                None, # TODO: staggering
                os.path.join('src/mountainAdvect/tracerField'),
                velocityField,
                os.path.join('src/schaerAdvect/T_init'),
                Timing(10000, 5000, timestep),
                fvSchemes, self.parallel, self.fast)

class MountainAdvectCollatedByMountainHeight:
    Test = collections.namedtuple('MountainAdvectCollatedByMountainHeightTest', ['name', 'mountainHeight', 'mesh', 'velocityField', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.mountainHeight, tests, fast,
                dummy=os.path.join('src/mountainAdvect/collatedErrors.mountainHeight.dummy'))

    def write(self, generator):
        l2 = os.path.join('10000/l2errorT.txt')
        self.collator.write(generator, l2)
        self.collator.s3upload(generator, [l2])

    def __str__(self):
        return self.case.name

class MountainAdvectCollatedByMeshSpacing:
    Test = collections.namedtuple('MountainAdvectCollatedByMeshSpacingTest', ['name', 'dx', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.dx, tests, fast,
                dummy=os.path.join('src/mountainAdvect/collatedErrors.meshSpacing.dummy'))

    def write(self, generator):
        self.collator.write(generator, Paths.timestep)
        self.collator.write(generator, Paths.courantNumber)
        self.collator.s3upload(generator, [Paths.timestep, Paths.courantNumber])

    def __str__(self):
        return self.case.name
