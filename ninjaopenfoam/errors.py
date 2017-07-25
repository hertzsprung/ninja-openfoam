class Errors:
    def __init__(self, case, time, field='T'):
        self.case = case
        self.time = str(time)
        self.field = field

    def write(self, generator):
        self.diff(generator)

        self.globalSum(generator, self.field + '_diff')
        self.globalSum(generator, self.field + '_analytic')

        self.l2(generator)
        self.linf(generator)

    def diff(self, generator):
        case = self.case 
        time = self.time
        field = self.field

        diff_field = field + '_diff'
        analytic_field = field + '_analytic'

        generator.w.build(
                outputs=case.path(time, diff_field),
                rule='sumFields',
                implicit=[
                    case.path(time, analytic_field),
                    case.path(time, field)
                ],
                variables={
                    "case": case,
                    "time": time,
                    "field": field
                }
        )
        generator.w.newline()

    def l2(self, generator):
        self.lp(generator, 'l2error{field}'.format(field=self.field))

        self.extractL2Error(generator, self.field + '_diff')
        self.extractL2Error(generator, self.field + '_analytic')

    def linf(self, generator):
        self.lp(generator, 'linferror{field}'.format(field=self.field))

        self.extractLinfError(generator, self.field + '_diff')
        self.extractLinfError(generator, self.field + '_analytic')

    def lp(self, generator, errorField):
        case = self.case
        time = self.time

        diff = case.path(time, errorField + '_diff.txt')
        analytic = case.path(time, errorField + '_analytic.txt')

        generator.w.build(
                outputs=case.path(time, errorField + '.txt'),
                rule='lperror',
                implicit=[diff, analytic],
                variables={
                    "diff": diff,
                    "analytic": analytic
                }
        )
        generator.w.newline()

    def globalSum(self, generator, field):
        case = self.case
        time = self.time

        generator.w.build(
                outputs=case.path(time, 'globalSum{field}.dat'.format(field=field)),
                rule='globalSum',
                implicit=[case.path(time, field)],
                variables={
                    "case": case,
                    "time": time,
                    "field": field
                }
        )
        generator.w.newline()

    def extractL2Error(self, generator, field):
        self.extractStat(generator, field, column=3, output='l2error')

    def extractLinfError(self, generator, field):
        self.extractStat(generator, field, column=4, output='linferror')

    def extractStat(self, generator, field, column, output):
        case = self.case
        time = self.time

        generator.w.build(
                outputs=case.path(time, '{output}{field}.txt'.format(
                    output=output,
                    field=field
                )),
                rule='extractStat',
                inputs=[case.path(time, 'globalSum{field}.dat'.format(field=field))],
                variables={"column": column}
        )
        generator.w.newline()
