import os

from .case import Case
from .paths import Paths

def Ang(name, case, file):
    return SIunitx(name, case, file, 'siunitx-ang')

def Num(name, case, file):
    return SIunitx(name, case, file, 'siunitx-num')

def Timestep(name, case, file=Paths.timestep):
    return SIunitx(name, case, file, 'siunitx-timestep')

def Velocity(name, case, file):
    return SIunitx(name, case, file, 'siunitx-velocity')

class SIunitx:
    def __init__(self, name, case, file, rule):
        self.name = name
        self.targetCase = Case(os.path.basename(case))
        self.sourceFile = os.path.join(case, file)
        self.targetFile = self.targetCase.path(os.path.splitext(file)[0] + '.tex')
        self.rule = rule

    def write(self, generator):
        generator.w.build(
                outputs=self.targetFile,
                rule=self.rule,
                inputs=self.sourceFile
        )
        generator.w.newline()

    def outputs(self):
        return [self.targetFile]

    def __str__(self):
        return self.name
