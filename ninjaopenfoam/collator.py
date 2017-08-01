class Collator:
    def __init__(self, case, independent, tests, fast, dummy):
        self.case = case
        self.independent = independent
        self.tests = tests
        self.fast = fast
        self.dummy = dummy

    def write(self, generator, dependent):
        g = generator

        if self.fast:
            g.w.build(
                    outputs=self.case.path(dependent),
                    rule='cp',
                    inputs=self.dummy)
        else:
            g.w.build(
                    outputs=self.case.path(dependent),
                    rule='collate',
                    implicit=[t.case.path(self.independent) for t in self.tests]
                            + [t.case.path(dependent) for t in self.tests],
                    variables={
                        "cases": [t.case.root for t in self.tests],
                        "independent": self.independent,
                        "dependent": dependent
                    }
            )

        g.w.newline()

    def s3upload(self, g, inputs):
        if not self.fast:
            g.s3upload(self.case, 
                    [self.case.path(i) for i in inputs] + [t.case.s3Uploaded for t in self.tests])

