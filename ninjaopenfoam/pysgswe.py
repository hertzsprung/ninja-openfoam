import os

class Intrusive:
    def __init__(self, name, output, testcase, basis, max_basis = 1,
            basis_dimensions = 1, truncate_basis = False, sample_indices = [],
            sample_points_min = None, sample_points_max = None,
            sample_points_num = None, end_time = None, elements = None,
            topography_peak = None):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.testcase = testcase
        self.basis = basis
        self.max_basis = max_basis
        self.basis_dimensions = basis_dimensions
        self.truncate_basis = truncate_basis
        self.sample_indices = [str(i) for i in sample_indices]
        self.sample_points_min = sample_points_min
        self.sample_points_max = sample_points_max
        self.sample_points_num = sample_points_num
        self.end_time = end_time
        self.elements = elements
        self.topography_peak = topography_peak

    def write(self, generator):
        variables = {
                'root': self.output,
                'testcase': self.testcase,
                'basis': self.basis,
                'max_basis': self.max_basis,
                'basis_dimensions': self.basis_dimensions}

        if self.truncate_basis:
            variables['truncate_basis'] = '--truncate-basis'

        if self.end_time:
            variables['end_time'] = '--end-time ' + str(self.end_time)

        if self.elements:
            variables['elements'] = '--elements ' + str(self.elements)

        if self.topography_peak is not None:
            variables['topography_peak'] = '--topography-peak ' + \
                    str(self.topography_peak)

        if not self.sample_indices:
            rule = 'pysgswe-intrusive'
        else:
            variables['sample_indices'] = ' '.join(self.sample_indices)

            if self.sample_points_min is None:
                rule = 'pysgswe-intrusive-sample-quadrature-points'
            else:
                rule = 'pysgswe-intrusive-sample-smooth-points'
                variables['sample_points'] = ' '.join([
                    str(self.sample_points_min),
                    str(self.sample_points_max),
                    str(self.sample_points_num)])

        generator.w.build(
                self.outputs(),
                rule,
                variables=variables)

    def outputs(self):
        outputs = [os.path.join(self.output, file)
                for file in ['statistics.initial.dat', 'statistics.end.dat',
                    'cfl.dat', 'quadrature-point-solutions.dat']]

        for i in self.sample_indices:
            outputs.append(os.path.join(self.output,
                'response-curve.quadrature-points.' + i + '.dat'))
            outputs.append(os.path.join(self.output,
                'quadrature-point-time-series.' + i + '.dat'))
            if self.sample_points_min is not None:
                outputs.append(os.path.join(self.output,
                    'response-curve.smooth.' + i + '.dat'))

        return outputs

    def __str__(self):
        return self.name

class Nonintrusive:
    def __init__(self, name, output, sample_indices = [], max_level = None,
            sample_uniform_min = None, sample_uniform_max = None,
            sample_uniform_num = None):
        self.name = name
        self.output = os.path.join('$builddir', output)
        self.sample_indices = [str(i) for i in sample_indices]
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

        if self.sample_indices:
            variables['sample_indices'] = '--response-curves ' + \
                    ' '.join(self.sample_indices)

        generator.w.build(
                self.outputs(),
                rule,
                variables=variables)

    def outputs(self):
        outputs = []

        for i in self.sample_indices:
            outputs.append(os.path.join(self.output,
                'response-curve.quadrature-points.' + i + '.dat'))

        return outputs

    def __str__(self):
        return self.name
