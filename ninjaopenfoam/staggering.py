class Lorenz:
    theta = 'theta'
    thetaDiff = 'theta_diff'
    thetaAnalytic = 'theta_analytic'

    solverRule = 'exnerFoamH'
    exnerRule = 'setExnerBalancedH'
    stratifiedThetaRule = 'setTheta'
    perturbedThetaRule = 'setPerturbedTheta'

    def __init__(self, thetaInit, T_init=None):
        self.thetaInit = thetaInit
        self.T_init = T_init

    def thetaInits(self, case):
        return [case.thetaInit]

    def thetaOutputs(self):
        return ['theta']

    def T_inits(self, case):
        return [case.T_init]

    def copyThetaInits(self, generator, case):
        generator.copy(self.thetaInit, case.thetaInit)

    def copyT_Inits(self, generator, case):
        if self.T_init is None:
            raise ValueError('T_init not specified')

        generator.copy(self.T_init, case.T_init)

class CharneyPhillips:
    theta = 'thetaf'
    thetaDiff = 'thetaf_diff'
    thetaAnalytic = 'thetaf_analytic'

    solverRule = 'exnerFoamCP'
    exnerRule = 'setExnerBalancedCP'
    stratifiedThetaRule = 'setThetaCP'

    def __init__(self, thetaInit, thetafInit):
        self.thetaInit = thetaInit
        self.thetafInit = thetafInit

    def thetaInits(self, case):
        return [case.thetaInit, case.thetafInit]

    def thetaOutputs(self):
        return ['theta', 'thetaf']

    def copyThetaInits(self, generator, case):
        generator.copy(self.thetaInit, case.thetaInit)
        generator.copy(self.thetafInit, case.thetafInit)
