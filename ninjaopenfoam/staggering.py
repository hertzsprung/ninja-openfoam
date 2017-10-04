class Lorenz:
    theta = 'theta'
    thetaDiff = 'theta_diff'
    thetaAnalytic = 'theta_analytic'

    solverRule = 'exnerFoamH'
    exnerRule = 'setExnerBalancedH'
    thetaRule = 'setTheta'

    def __init__(self, thetaInit):
        self.thetaInit = thetaInit

    def thetaInits(self, case):
        return [case.thetaInit]

    def copyThetaInits(self, generator, case):
        generator.copy(self.thetaInit, case.thetaInit)

class CharneyPhillips:
    theta = 'thetaf'
    thetaDiff = 'thetaf_diff'
    thetaAnalytic = 'thetaf_analytic'

    solverRule = 'exnerFoamCP'
    exnerRule = 'setExnerBalancedCP'
    thetaRule = 'setThetaCP'

    def __init__(self, thetaInit, thetafInit):
        self.thetaInit = thetaInit
        self.thetafInit = thetafInit

    def thetaInits(self, case):
        return [case.thetaInit, case.thetafInit]

    def copyThetaInits(self, generator, case):
        generator.copy(self.thetaInit, case.thetaInit)
        generator.copy(self.thetafInit, case.thetafInit)
