import os

class Gnuplot:
    def __init__(self, name, output, plot, data=[]):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.plot = plot
        self.data = data

    def write(self, generator):
        generator.w.build(
                self.output + '.tex',
                'gnuplot',
                self.plot,
                implicit=self.data,
                implicit_outputs=[self.output + '.eps'])

    def outputs(self):
        return [self.output + ext for ext in ['.tex', '.eps']]

    def __str__(self):
        return self.name
