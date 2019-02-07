import os

class Basis:
    def __init__(self, name, output, max_level):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.max_level = max_level

    def write(self, generator):
        generator.w.build(
                self.outputs(),
                rule='pysg-basis',
                variables={
                    'output': self.output,
                    'max_level': self.max_level})

    def outputs(self):
        outputs = []

        for i in range(2**self.max_level):
            outputs.append(os.path.join(self.output,
                'basis_func.' + str(i) + '.dat'))

        return outputs

    def __str__(self):
        return self.name
