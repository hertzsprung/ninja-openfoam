class Collator:
    def __init__(self, case, independent, tests, fast, dummy):
        self.case = case
        self.independent = independent
        self.tests = tests
        self.fast = fast
        self.dummy = dummy

    def write(self, generator, dependent):
        if self.fast:
            generator.w.build(
                    outputs=self.case.path(dependent),
                    rule='cp',
                    inputs=dummy)
        else:
            generator.w.build(
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

        generator.w.newline()
