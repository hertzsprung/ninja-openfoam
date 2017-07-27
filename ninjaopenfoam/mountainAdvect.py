import collections
import os

from .advect import Advect
from .case import Case
from .collator import Collator
from .paths import Paths

class MountainAdvectBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, dx, fvSchemes, tests):
        tests = [self.test(t.name, dx, t.mountainHeight, t.mesh, t.timestep, fvSchemes)
                for t in tests]
        return MountainAdvectCollated(name, tests, self.fast)

    def test(self, name, dx, mountainHeight, mesh, timestep, fvSchemes):
        if self.fast:
            mesh = self.fastMesh
            timestep = 40
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return Advect(name, dx, mountainHeight, mesh, 
                os.path.join('src/mountainAdvect/tracerField'),
                os.path.join('src/mountainAdvect/velocityField'),
                timestep, fvSchemes, self.parallel, self.fast)

class MountainAdvectCollated:
    Test = collections.namedtuple('MountainAdvectCollatedTest', ['name', 'mountainHeight', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.mountainHeight, tests, fast,
                dummy=os.path.join('src/mountainAdvect/collatedErrors.mountainHeight.dummy'))

    def write(self, generator):
        self.collator.write(generator, os.path.join('10000/l2errorT.txt'))

    def __str__(self):
        return self.case.name

