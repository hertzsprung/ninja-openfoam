class StratifiedThermalField:
    def write(self, generator, case, staggering):
        g = generator
        g.w.build(
                outputs=[case.path('0', theta) for theta in staggering.thetaOutputs()],
                rule=staggering.stratifiedThetaRule,
                implicit=case.polyMesh + case.systemFiles + \
                    staggering.thetaInits(case) + [
                    case.environmentalProperties,
                    case.thermophysicalProperties
                ],
                variables={'case': case}
        )
        g.w.newline()

class PerturbedThermalField:
    def __init__(self, tracerFieldDict):
        self.tracerFieldDict = tracerFieldDict

    def write(self, generator, case, staggering):
        g = generator
        g.w.build(
                outputs=case.path('0', staggering.theta),
                rule=staggering.perturbedThetaRule,
                implicit=case.polyMesh + case.systemFiles + \
                    staggering.T_inits(case) +
                    staggering.thetaInits(case) + [
                    case.tracerFieldDict,
                    case.environmentalProperties,
                    case.thermophysicalProperties
                ],
                variables={'case': case},
                implicit_outputs=[
                    case.path('0/theta.perturbation'),
                    case.path('0/theta.background')
                ]
        )
        g.w.newline()

        g.copy(case.path('0/theta.perturbation'), case.path('0/theta_diff'))
        g.copy(self.tracerFieldDict, case.tracerFieldDict)
        staggering.copyT_Inits(g, case)
