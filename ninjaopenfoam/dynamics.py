from .solver import SolverExecution

import os

class DynamicsExecution:
    def __init__(
            self,
            case,
            mesh,
            timing,
            staggering,
            thermalField,
            initialUf,
            exnerInit,
            environmentalProperties,
            thermophysicalProperties,
            fvSchemes,
            fvSolution,
            sponge,
            parallel):
        self.case = case
        self.mesh = mesh
        self.timing = timing
        self.staggering = staggering
        self.thermalField = thermalField
        self.initialUf = initialUf
        self.exnerInit = exnerInit
        self.environmentalProperties = environmentalProperties
        self.thermophysicalProperties = thermophysicalProperties
        self.fvSchemes = fvSchemes
        self.fvSolution = fvSolution
        self.sponge = sponge
        self.parallel = parallel

    def write(self, generator):
        case = self.case
        staggering = self.staggering
        g = generator
        endTime = str(self.timing.endTime)

        solver = SolverExecution(
                g,
                case,
                self.parallel,
                os.path.join("src/advect/decomposeParDict.template")
        )

        implicit = case.polyMesh + case.systemFiles + [
            case.path('0/Uf'),
            case.path('0', staggering.theta),
            case.path('0/Exner'),
            case.environmentalProperties,
            case.thermophysicalProperties
        ]

        if self.sponge:
            implicit += [case.sponge]

        solver.solve(
            outputs=[
                case.energy,
                case.path(endTime, 'Uf')
            ] + \
            [case.path(endTime, theta) for theta in staggering.thetaOutputs()],
            rule=staggering.dynamicsSolverRule,
            implicit=implicit
        )

        self.thermalField.write(generator, case, staggering)

        g.w.build(
                outputs=case.path('0/Exner'),
                rule=staggering.exnerRule,
                implicit=case.polyMesh + case.systemFiles + [
                    case.exnerInit,
                    case.path('0', staggering.theta),
                    case.environmentalProperties,
                    case.thermophysicalProperties
                ],
                variables={'case': case}
        )
        g.w.newline()

        if self.sponge:
            g.w.build(
                    outputs=case.sponge,
                    rule='createSpongeLayer',
                    implicit=case.polyMesh + case.systemFiles + \
                        [case.environmentalProperties],
                    variables={'case': case}
            )
            g.w.newline()

        g.copy(self.initialUf, case.path('0/Uf'))
        staggering.copyThetaInits(g, case)
        g.copy(self.exnerInit, case.exnerInit)
        g.copy(self.environmentalProperties, case.environmentalProperties)
        g.copy(self.thermophysicalProperties, case.thermophysicalProperties)
        g.copy(self.fvSchemes, case.fvSchemes)
        g.copy(self.fvSolution, case.fvSolution)
        g.copyMesh(source=self.mesh.case, target=case)
        g.controlDict(case, self.timing)

