import os

class Intrusive:
    def __init__(self, name, output, basis, sample_indices, max_basis,
            sample_points_min = None, sample_points_max = None,
            sample_points_num = None):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.basis = basis
        self.sample_indices = sample_indices
        self.max_basis = max_basis
        self.sample_points_min = sample_points_min
        self.sample_points_max = sample_points_max
        self.sample_points_num = sample_points_num

    def write(self, generator):
        variables = {
                'root': self.output,
                'basis': self.basis,
                'max_basis': self.max_basis}

        if self.sample_points_min is not None:
            rule = 'pysgswe-intrusive-sample-points'
            variables['sample_points'] = ' '.join([
                str(self.sample_points_min),
                str(self.sample_points_max),
                str(self.sample_points_num)])
        else:
            rule = 'pysgswe-intrusive'

        generator.w.build(
                self.outputs(),
                rule,
                variables=variables)

    def outputs(self):
        outputs = []

        for i in self.sample_indices:
            outputs.append(os.path.join(self.output,
                'response-curve.quadrature-points.' + str(i) + '.dat'))
            if self.sample_points_min is not None:
                outputs.append(os.path.join(self.output,
                    'response-curve.smooth.' + str(i) + '.dat'))

        return outputs

    def __str__(self):
        return self.name

class Nonintrusive:
    def __init__(self, name, output, sample_indices, max_level = None,
            sample_uniform_min = None, sample_uniform_max = None,
            sample_uniform_num = None):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.sample_indices = sample_indices
        self.max_level = max_level
        self.sample_uniform_min = sample_uniform_min
        self.sample_uniform_max = sample_uniform_max
        self.sample_uniform_num = sample_uniform_num

    def write(self, generator):
        variables = {'root': self.output}

        if self.sample_uniform_min is not None:
            rule = 'pysgswe-nonintrusive-sample-uniform'
            variables['sample_uniform'] = ' '.join([
                str(self.sample_uniform_min),
                str(self.sample_uniform_max),
                str(self.sample_uniform_num)])
        else:
            rule = 'pysgswe-nonintrusive'
            variables['max_level'] = self.max_level

        generator.w.build(
                self.outputs(),
                rule,
                variables=variables)

    def outputs(self):
        outputs = []

        for i in self.sample_indices:
            outputs.append(os.path.join(self.output,
                'response-curve.quadrature-points.' + str(i) + '.dat'))

        return outputs

    def __str__(self):
        return self.name
