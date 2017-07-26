class SphericalMesh:
    def __init__(self, case):
        self.case = case

    def write(self, generator):
        g = generator
        case = self.case

        g.w.build(
                outputs=case.averageEquatorialSpacing,
                rule="averageEquatorialSpacing",
                inputs=case.averageCellCentreDistance,
        )
        g.w.newline()

        g.w.build(
                outputs=case.averageCellCentreDistance,
                rule="averageCellCentreDistance",
                implicit=case.polyMesh + case.systemFiles,
                variables={"case": case}
        )
        g.w.newline()
