class Lorenz:
    theta = 'theta'
    thetaDiff = 'theta_diff'
    thetaAnalytic = 'theta_analytic'

    solverRule = 'exnerFoamH'
    exnerRule = 'setExnerBalancedH'
    thetaRule = 'setTheta'

    def thetaInit(self, case):
        return case.thetaInit

class CharneyPhillips:
    theta = 'thetaf'
    thetaDiff = 'thetaf_diff'
    thetaAnalytic = 'thetaf_analytic'

    solverRule = 'exnerFoamCP'
    exnerRule = 'setExnerBalancedCP'
    thetaRule = 'setThetaCP'

    def thetaInit(self, case):
        return case.thetafInit
