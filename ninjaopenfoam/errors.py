class Errors:
    def __init__(self, case, time, field='T'):
        self.case = case
        self.time = str(time)
        self.field = field

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
        case = self.case
        time = self.time

        diff = case.path(time, 'l2error{field}_diff.txt'.format(field=self.field))
        analytic = case.path(time, 'l2error{field}_analytic.txt'.format(field=self.field))

        generator.w.build(
                outputs=case.path(time, 'l2error{field}.txt'.format(field=self.field)),
                rule='lperror',
                implicit=[diff, analytic],
                variables={
                    "diff": diff,
                    "analytic": analytic
                }
        )
        generator.w.newline()

#        self.globalSum(field + '_diff')
#        self.globalSum(field + '_analytic')

#        self.extractL2Error(field + '_diff')
#        self.extractL2Error(field + '_analytic')

    def globalSum(self, field):
        case = self.case
        time = self.time

        self.w.build(
                outputs=case.path(time, 'globalSum{field}.dat'.format(field=field)),
                rule='globalSum',
                implicit=[case.path(time, field)],
                variables={
                    "case": case,
                    "time": time,
                    "field": field
                }
        )
        self.w.newline()

    def extractL2Error(self, field):
        self.extractStat(field, column=3, output='l2error')

    def extractStat(self, field, column, output):
        case = self.case
        time = self.time

        self.w.build(
                outputs=case.path(time, '{output}{field}.txt'.format(
                    output=output,
                    field=field
                )),
                rule='extractStat',
                inputs=[case.path(time, 'globalSum{field}.dat'.format(field=field))],
                variables={"column": column}
        )
        self.w.newline()
