class Lorenz:
    theta = 'theta'
    T = 'T'
    T_analytic = 'T_analytic'

    advectionSolverRule = 'advectionFoam'
    dynamicsSolverRule = 'exnerFoamH'
    exnerRule = 'setExnerBalancedH'
    stratifiedThetaRule = 'setTheta'
    perturbedThetaRule = 'setPerturbedTheta'

    def __init__(self, thetaInit, T_init):
        self.thetaInit = thetaInit
        self.T_init = T_init

    @classmethod
    def advect(cls, T_init):
        return cls(None, T_init)

    @classmethod
    def dynamics(cls, thetaInit, T_init=None):
        return cls(thetaInit, T_init)

    def thetaInits(self, case):
        return [case.thetaInit]

    def thetaOutputs(self):
        return ['theta']

    def T_inits(self, case):
        return [case.T_init]

    def copyThetaInits(self, generator, case):
        if self.thetaInit is None:
            raise ValueError('thetaInit not specified')

        generator.copy(self.thetaInit, case.thetaInit)

    def copyT_Inits(self, generator, case):
        if self.T_init is None:
            raise ValueError('T_init not specified')

        generator.copy(self.T_init, case.T_init)

class CharneyPhillips:
    theta = 'thetaf'
    T = 'Tf'
    T_analytic = 'Tf_analytic'

    advectionSolverRule = 'advectiveFoamF'
    dynamicsSolverRule = 'exnerFoamCP'
    exnerRule = 'setExnerBalancedCP'
    stratifiedThetaRule = 'setThetaCP'
    perturbedThetaRule = 'setPerturbedThetaCP'

    def __init__(self, thetaInit, thetafInit, T_init=None, Tf_init=None):
        self.thetaInit = thetaInit
        self.thetafInit = thetafInit
        self.T_init = T_init
        self.Tf_init = Tf_init

    def thetaInits(self, case):
        return [case.thetaInit, case.thetafInit]

    def thetaOutputs(self):
        return ['theta', 'thetaf']

    def T_inits(self, case):
        return [case.T_init, case.Tf_init]

    def copyThetaInits(self, generator, case):
        if self.thetaInit is None:
            raise ValueError('thetaInit not specified')

        if self.thetafInit is None:
            raise ValueError('thetafInit not specified')

        generator.copy(self.thetaInit, case.thetaInit)
        generator.copy(self.thetafInit, case.thetafInit)

    def copyT_Inits(self, generator, case):
        if self.T_init is None:
            raise ValueError('T_init not specified')

        if self.Tf_init is None:
            raise ValueError('Tf_init not specified')

        generator.copy(self.T_init, case.T_init)
        generator.copy(self.Tf_init, case.Tf_init)
