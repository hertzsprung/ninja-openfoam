from .case import Case

import os

class LaTeXSubstitution:
    def __init__(self, name, output, input, data=[]):
        self.case = Case(name)
        self.output = os.path.join('$builddir', output + '.tex')
        self.input = input + '.tex'
        self.data = data

    def write(self, generator):
        g = generator

        g.w.build(
                outputs=self.output,
                rule='latex-substitute',
                inputs=self.input,
                implicit=self.data
        )
        g.w.newline()

    def outputs(self):
        return [self.output]

    def __str__(self):
        return self.case.name

