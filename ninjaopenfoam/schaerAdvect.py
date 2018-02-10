import collections
import os

from .advect import Advect
from .case import Case
from .collator import Collator
from .paths import Paths
from .staggering import Lorenz
from .timing import Timing

class SchaerAdvectBuilder:
    def __init__(self, mountainHeight, tracerField, velocityField, parallel, fast, fastMesh):
        self.mountainHeight = mountainHeight
        self.tracerField = tracerField
        self.velocityField = velocityField
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, fvSchemes, tests,
            controlDict=Paths.defaultControlDict, solverRule=None):
        tests = [self.test(t.name, t.dx, t.mesh, t.timestep,
                        fvSchemes, controlDict, solverRule)
                for t in tests]
        return SchaerAdvectCollated(name, tests, self.fast)

    def test(self, name, dx, mesh, timestep,
            fvSchemes, controlDict, solverRule):
        if self.fast:
            mesh = self.fastMesh
            timestep = 40
            fvSchemes = os.path.join('src/schaerAdvect/linearUpwind')
            controlDict = Paths.defaultControlDict
            solverRule = None

        return Advect(name, dx, self.mountainHeight, mesh, 
                Lorenz.advect(os.path.join('src/schaerAdvect/T_init')),
                self.tracerField,
                self.velocityField,
                Timing(10000, 5000, timestep),
                fvSchemes, self.parallel, self.fast, controlDict, solverRule)

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

