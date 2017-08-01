import collections
import os

from .advect import Advect
from .case import Case
from .collator import Collator
from .paths import Paths

class SchaerAdvectBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, mountainHeight, fvSchemes, tests):
        tests = [self.test(t.name, t.dx, mountainHeight, t.mesh, t.timestep, fvSchemes)
                for t in tests]
        return SchaerAdvectCollated(name, tests, self.fast)

    def test(self, name, dx, mountainHeight, mesh, timestep, fvSchemes):
        if self.fast:
            mesh = self.fastMesh
            timestep = 40
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')

        return Advect(name, dx, mountainHeight, mesh, 
                os.path.join('src/schaerAdvect/tracerField'),
                os.path.join('src/schaerAdvect/velocityField'),
                timestep, fvSchemes, self.parallel, self.fast)

class SchaerAdvectCollated:
    Test = collections.namedtuple('SchaerAdvectCollatedTest', ['name', 'dx', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.dx, tests, fast,
                dummy=os.path.join('src/schaerAdvect/collatedErrors.dummy'))

    def write(self, generator):
        l2 = os.path.join('10000/l2errorT.txt')
        linf = os.path.join('10000/linferrorT.txt')

        self.collator.write(generator, l2)
        self.collator.write(generator, linf)
        self.collator.s3upload(generator, [l2, linf])
        
    def __str__(self):
        return self.case.name

