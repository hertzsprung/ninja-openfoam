class Sample:
    def __init__(self, case, time, field, sampleDict, suffix='.sampleLine.dat'):
        self.case = case
        self.time = str(time)
        self.field = field
        self.sampleDict = sampleDict
        self.suffix = suffix
    
    def write(self, generator):
        case = self.case

        line = case.path('postProcessing/sampleDict/{time}/line_{field}.xy'
                    .format(time=self.time, field=self.field))

        generator.copy(line, case.path(self.time, self.field + self.suffix))
        
        generator.w.build(
                outputs=line,
                rule='sample',
                implicit=[
                    case.path(self.time, self.field),
                    case.sampleDict
                ],
                variables={
                    "case": case,
                    "time": self.time
                }
        )
        generator.w.newline()

        generator.copy(self.sampleDict, case.sampleDict)
