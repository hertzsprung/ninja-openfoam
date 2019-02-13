import os

class Tabulate:
    def __init__(self, name, output):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.entries = []
        self.inputs = []

    def add_entry(self, value, filename):
        filename = os.path.join('$builddir', filename)
        self.entries.append((value, filename))
        self.inputs.append(filename)

    def write(self, generator):
        entries = ''
        for value, filename in self.entries:
            entries = entries + str(value) + ' ' + filename + ' '

        generator.w.build(
                self.output,
                'tabulate',
                self.inputs,
                variables={'entries': entries})

    def outputs(self):
        return [self.output]

    def __str__(self):
        return self.name
