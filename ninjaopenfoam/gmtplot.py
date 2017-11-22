from .case import Case, CopyCase
from .paths import Paths

import os

class GmtPlot:
    def __init__(self, name, plot, case, time, data=[], colorBar=None):
        self.name = name
        self.case = case
        self.time = str(time)
        self.data = data
        self.colorBar = None if colorBar is None else case.path(colorBar)

        self.targetPlot = self.case.path('constant/gmtDicts', plot)
        self.output = self.case.path(self.time, plot) + '.pdf'

    def write(self, generator):
        g = generator

        outputs = [self.output]
        if self.colorBar:
            outputs += [self.colorBar]
        
        g.w.build(
                outputs,
                'gmtFoam',
                self.targetPlot,
                implicit=[self.case.gmtConf]
                        + [self.case.path(d) for d in self.data]
                        + self.case.polyMesh
                        + self.case.systemFiles,
                variables={'case': self.case, 'time': self.time})
        g.w.newline()

        if self.colorBar:
            g.w.build(
                self.case.path(self.name + '-colorBar.eps'),
                'gmtFoam-colorBar',
                self.colorBar,
                implicit=self.output)
            g.w.newline()

    def outputs(self):
        o = [self.output]
        if self.colorBar:
            o += [self.case.path(self.name + '-colorBar.eps')]
        return o

    def __str__(self):
        return self.name

class GmtPlotCopyCase:
    def __init__(self, name, source, target, plots, files=[], renamedFiles={}):
        self.name = name
        self.copyCase = CopyCase(name, source, target, files + ['system/controlDict'], renamedFiles)
        self.targetCase = Case(name, prefix=target)
        self.plots = plots

    def write(self, generator):
        g = generator

        self.copyCase.write(g)

        g.copy(os.path.join('src/fvSchemes.gmtPlot'), self.targetCase.fvSchemes)
        g.copy(os.path.join('src/fvSolution.gmtPlot'), self.targetCase.fvSolution)

        for p in self.plots:
            sourcePlot = p
            plotBasename = os.path.basename(os.path.splitext(sourcePlot)[0])
            targetPlot = self.targetCase.path('constant/gmtDicts', plotBasename)

            g.copy(sourcePlot, targetPlot)

        g.copy('src/gmt.conf', self.targetCase.gmtConf)

    def __str__(self):
        return self.name
