import collections
import os

from .advect import Advect
from .case import Case
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
        self.fast = fast

    def write(self, generator):
        g = generator

        self.collateErrors(generator, 'l2errorT.txt')
        self.collateErrors(generator, 'linferrorT.txt')

    def collateErrors(self, generator, file):
        endTime = '10000'

        if self.fast:
            generator.w.build(
                    outputs=self.case.path(endTime, file),
                    rule='cp',
                    inputs=os.path.join('src/schaerAdvect/collatedErrors.dummy'))
        else:
            generator.w.build(
                    outputs=self.case.path(endTime, file),
                    rule='collate',
                    implicit=[t.case.dx for t in self.tests]
                            + [t.case.path(endTime, file) for t in self.tests],
                    variables={
                        "cases": [t.case.root for t in self.tests],
                        "independent": Paths.dx,
                        "dependent": os.path.join(endTime, file)
                    }
            )

        generator.w.newline()
        
    def __str__(self):
        return self.case.name

