import os

from .case import Case

class Ang:
    def __init__(self, name, case, file):
        self.name = name
        self.targetCase = Case(os.path.basename(case))
        self.sourceFile = os.path.join(case, file)
        self.targetFile = self.targetCase.path(os.path.splitext(file)[0] + '.tex')

    def write(self, generator):
        generator.w.build(
                outputs=self.targetFile,
                rule='siunitx-ang',
                inputs=self.sourceFile
        )
        generator.w.newline()

    def outputs(self):
        return [self.targetFile]

    def __str__(self):
        return self.name

class Num:
    def __init__(self, name, case, file):
        self.name = name
        self.targetCase = Case(os.path.basename(case))
        self.sourceFile = os.path.join(case, file)
        self.targetFile = self.targetCase.path(os.path.splitext(file)[0] + '.tex')

    def write(self, generator):
        generator.w.build(
                outputs=self.targetFile,
                rule='siunitx-num',
                inputs=self.sourceFile
        )
        generator.w.newline()

    def outputs(self):
        return [self.targetFile]

    def __str__(self):
        return self.name
