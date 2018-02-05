import collections
import os

from .case import Case
from .collator import Collator
from .errors import Errors
from .paths import Paths
from .timing import Timing

class DeformationPlaneBuilder:
    def __init__(self, parallel, fast, fastMesh):
        self.parallel = parallel
        self.fast = fast
        self.fastMesh = fastMesh

    def collated(self, name, fvSchemes, tests,
            controlDict=None, solverRule=None):
        tests = [self.test(t.name, t.dx, t.mesh, t.timestep,
                        fvSchemes, controlDict, solverRule)
                for t in tests]
        return DeformationPlaneCollated(name, tests, self.fast)

    def test(self, name, dx, mesh, timestep,
            fvSchemesGhost, controlDict, solverRule):
        fvSchemesPrimary = os.path.join('src/deformationPlane/fvSchemes.primary')

        if self.fast:
            mesh = self.fastMesh
            timestep = 0.004
            fvSchemesGhost = os.path.join('src/deformationPlane/linearUpwind')
            controlDict = None
            solverRule = None

        return DeformationPlaneAdvect(name, dx, mesh, timestep,
                fvSchemesPrimary, fvSchemesGhost, self.parallel, self.fast,
                controlDict, solverRule)

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
    def __init__(self, name, dx, mesh, timestep, fvSchemesPrimary,
            fvSchemesGhost, parallel, fast,
            controlDict = None, solverRule = None):
        self.case = Case(name)
        self.dx = dx
        self.mesh = mesh
        self.timing = Timing(5, 1, timestep)
        self.fvSchemesPrimary = fvSchemesPrimary
        self.fvSchemesGhost = fvSchemesGhost
        self.fvSolution = os.path.join('src/deformationPlane/fvSolution')
        self.controlDict = controlDict or os.path.join('src/deformationPlane/controlDict.template')
        self.setGaussiansDict = os.path.join('src/deformationPlane/setGaussiansDict')
        self.deformationalAdvectionDict = os.path.join('src/deformationPlane/deformationalAdvectionDict')
        self.solverRule = solverRule or 'scalarDeformation'

    def write(self, generator):
        g = generator
        case = self.case

        self.lperrors(g)

        g.w.build(
                outputs=case.path('5/T'),
                rule=self.solverRule,
                implicit=case.polyMesh + case.ghostPolyMesh + case.systemFiles + [
                    case.path('system/ghostMesh/fvSchemes'),
                    case.path('system/ghostMesh/fvSolution'),
                    case.path('0/T'),
                    case.path('0/phi'),
                    case.path('0/ghostMesh/TGhost'),
                    case.path('0/ghostMesh/phiGhost'),
                    case.deformationalAdvectionDict
                ],
                variables={'case': case})
        g.w.newline()

        g.w.build(
                outputs=case.path('0/T'),
                rule='setGaussians',
                implicit=case.polyMesh + case.systemFiles + \
                        [case.setGaussiansDict],
                variables={'case': case})
        g.w.newline()

        g.w.build(self.case.dx, 'echo', variables={'string': str(self.dx)})
        g.copyMesh(source=self.mesh.case, target=case)
        g.copyAll(Paths.ghostPolyMesh, self.mesh.case, case)
        g.copy(self.fvSchemesPrimary, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.copy(self.fvSchemesGhost, case.path('system/ghostMesh/fvSchemes'))
        g.copy(self.fvSolution, case.path('system/ghostMesh/fvSolution'))
        g.copy(self.setGaussiansDict, case.setGaussiansDict)
        g.copy(self.deformationalAdvectionDict, case.deformationalAdvectionDict)
        g.copy(os.path.join('src/deformationPlane/phi'), case.path('0/phi'))
        g.copy(os.path.join('src/deformationPlane/phiGhost'), case.path('0/ghostMesh/phiGhost'))
        g.copy(os.path.join('src/deformationPlane/TGhost'), case.path('0/ghostMesh/TGhost'))
        g.controlDict(case, self.timing, self.controlDict)

    def lperrors(self, generator):
        g = generator
        case = self.case
        endTime = str(self.timing.endTime)

        errors = Errors(self.case, endTime, 'T')
        errors.write(g)

        g.copy(case.path('0/T'), case.path(endTime, 'T_analytic'))
        g.w.newline()

    def __str__(self):
        return self.case.name
