from .case import Case
from .paths import Paths

import os

class GmtPlot:
    def __init__(self, name, plot, case, time, data=[]):
        self.name = name
        self.sourceCase = case
        self.targetCase = Case(self.sourceCase.name)
        self.time = str(time)
        self.data = data

        plotBasename = os.path.basename(os.path.splitext(plot)[0])

        self.sourcePlot = plot
        self.targetPlot = self.targetCase.path('constant/gmtDicts', plotBasename)
        self.output = self.targetCase.path(self.time, plotBasename) + '.pdf'

    def write(self, generator):
        g = generator
        
        g.w.build(
                self.output,
                'gmtFoam',
                self.targetPlot,
                implicit=['gmt.conf']
                        + [self.targetCase.path(d) for d in self.data]
                        + self.targetCase.polyMesh
                        + self.targetCase.systemFiles,
                variables={'case': self.targetCase, 'time': self.time})
        g.w.newline()

        g.copy(self.sourcePlot, self.targetPlot)
        g.copyAll(Paths.polyMesh, self.sourceCase, self.targetCase)
        g.copy(self.sourceCase.controlDict, self.targetCase.controlDict)
        g.copy(os.path.join('src/thesis/fvSchemes.plotMesh'), self.targetCase.fvSchemes)
        g.copy(os.path.join('src/thesis/fvSolution.plotMesh'), self.targetCase.fvSolution)

        for d in self.data:
            g.copy(self.sourceCase.path(d), self.targetCase.path(d))

    def outputs(self):
        return [self.output]

    def __str__(self):
        return self.name
