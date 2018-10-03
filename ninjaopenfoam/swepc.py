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
                self.output + '.dat',
                'swepc',
                variables={
                    'testCase': self.testCase,
                    'solver': self.solver,
                    'degree': self.degree,
                    'elements': self.elements,
                    'endTime': self.endTime,
                    'dt': self.dt})

    def outputs(self):
        return [self.output + '.dat']

    def __str__(self):
        return self.name

class SWEMonteCarlo:
    def __init__(self, name, output, testCase, solver, iterations, sampleIndex,
            elements, endTime, dt):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.testCase = testCase
        self.solver = solver
        self.iterations = iterations
        self.sampleIndex = sampleIndex
        self.elements = elements
        self.endTime = endTime
        self.dt = dt

    def write(self, generator):
        generator.w.build(
            os.path.join(self.output, 'flow.dat'),
            'swemc',
            implicit_outputs=[os.path.join(self.output, 'convergence.dat'),
                os.path.join(self.output, 'sample'+str(self.sampleIndex)+'.dat')],
            variables={
                'outputDir': self.output,
                'testCase': self.testCase,
                'solver': self.solver,
                'iterations': self.iterations,
                'sampleIndex': self.sampleIndex,
                'elements': self.elements,
                'endTime': self.endTime,
                'dt': self.dt})
    def outputs(self):
        return [os.path.join(self.output, file)
                for file in ['flow.dat', 'convergence.dat',
                    'sample'+str(self.sampleIndex)+'.dat']]

    def __str__(self):
        return self.name

