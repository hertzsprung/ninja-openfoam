import os

class SWEPC:
    def __init__(self, name, output, testCase, solver, degree, elements, endTime, dt):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.testCase = testCase
        self.solver = solver
        self.degree = degree
        self.elements = elements
        self.endTime = endTime
        self.dt = dt

    def write(self, generator):
        generator.w.build(
                self.output,
                'swepc',
                variables={
                    'testCase': self.testCase,
                    'solver': self.solver,
                    'degree': self.degree,
                    'elements': self.elements,
                    'endTime': self.endTime,
                    'dt': self.dt})

    def outputs(self):
        return [self.output]

    def __str__(self):
        return self.name
