from .case import Case
from .collator import Collator
from .dynamics import DynamicsExecution
from .paths import Paths
from .staggering import Lorenz
from .timing import Timing
from .thermalField import StratifiedThermalField

import collections
import os

class RestingBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collateByMountainHeight(self, name, fvSchemes, tests):
        tests = [self.test(t.name, t.mountainHeight, t.mesh, t.timestep, fvSchemes)
                for t in tests]
        return RestingCollated(name, tests, self.fast)

    def test(self, name, mountainHeight, mesh, timestep, fvSchemes):
        if self.fast:
            mesh = self.fastMesh
            timestep = 50
            fvSchemes = os.path.join('src/resting/linearUpwind')

        return Resting(name, mountainHeight, mesh, 
                timestep, fvSchemes, self.parallel, self.fast)

class RestingCollated:
    Test = collections.namedtuple('RestingCollated', ['name', 'mountainHeight', 'mesh', 'timestep'])

    def __init__(self, name, tests, fast):
        self.case = Case(name)
        self.tests = tests
        self.collator = Collator(self.case, Paths.mountainHeight, tests, fast,
                dummy=os.path.join('src/resting/collatedMaxW.dummy'))

    def write(self, generator):
        self.collator.write(generator, Paths.maxw)
        self.collator.write(generator, Paths.maxKE)
        self.collator.s3upload(generator, [Paths.maxw, Paths.maxKE])

    def __str__(self):
        return self.case.name

class Resting:
    def __init__(self, name, mountainHeight, mesh, timestep, fvSchemes, parallel, fast):
        self.case = Case(name)
        self.mountainHeight = mountainHeight
        self.fast = fast

        if fast:
            timing = Timing(500, 500, timestep)
        else:
            timing = Timing(21600, 10800, timestep)

        self.dynamicsExecution = DynamicsExecution(
                self.case,
                mesh,
                timing,
                Lorenz(os.path.join('src/resting/theta_init')),
                StratifiedThermalField(),
                os.path.join('src/resting/Uf'),
                os.path.join('src/resting/Exner_init'),
                os.path.join('src/resting/environmentalProperties'),
                os.path.join('src/resting/thermophysicalProperties'),
                fvSchemes,
                os.path.join('src/resting/fvSolution'),
                sponge=False,
                parallel=parallel)

    def write(self, generator):
        g = generator
        case = self.case

        g.w.build(
                outputs=case.maxw,
                rule='maxw',
                inputs=case.energy
        )
        g.w.newline()

        g.w.build(
                outputs=case.maxKE,
                rule='maxKE',
                inputs=case.energy
        )
        g.w.newline()

        self.dynamicsExecution.write(generator)

        g.w.build(self.case.mountainHeight, 'echo', variables={'string': str(self.mountainHeight)})

        if not self.fast:
            g.s3uploadCase(case, [case.maxw, case.maxKE])

    def __str__(self):
        return self.case.name
