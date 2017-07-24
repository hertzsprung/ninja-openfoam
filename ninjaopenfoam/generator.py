from . import syntax
from .paths import Paths

import datetime
import os
import sys
from pkg_resources import resource_filename

class Generator:
    def __init__(self, out):
        self.w = syntax.Writer(out)

    def controlDict(self, case, timing):
        self.w.build(
                outputs=case.controlDict,
                rule="gen-controlDict",
                inputs=os.path.join("src", "controlDict.template"),
                variables={
                    "endTime": timing.endTime,
                    "writeInterval": timing.writeInterval,
                    "timestep": timing.timestep,
                }
        )
        self.w.newline()

    def copy(self, source, target):
        self.w.build(outputs=str(target), rule="cp", inputs=str(source))

    def copyAll(self, files, source, target):
        for f in files:
            self.copy(os.path.join(str(source), f), os.path.join(str(target), f))

    def copyMesh(self, source, target):
        self.copyAll(Paths.polyMesh, source, target)

    def header(self):
        self.w.comment("Generated by \"{}\"".format(" ".join(sys.argv)))
        self.w.comment("at {}".format(datetime.datetime.utcnow().isoformat()))
        self.w.newline()

    def initialTracer(self, case, tracerFieldDict, T_init):
        self.w.build(
                outputs=case.path("0", "T"),
                rule="setInitialTracerField",
                implicit=case.polyMesh + case.systemFiles +
                        [case.tracerFieldDict, case.T_init],
                variables={"case": case}
        )
        self.w.newline()
        self.copy(tracerFieldDict, case.tracerFieldDict)
        self.copy(T_init, case.T_init)
        self.w.newline()

    def s3upload(self, case, implicit=[]):
        implicit += case.polyMesh + case.systemFiles
        self.w.build(
                outputs=case.path("s3.uploaded"),
                rule="s3-upload",
                implicit=implicit,
                variables={"source": case}
        )
        self.w.newline()

    def scriptRule(self, name, command, description=None, pool=None):
        script, args = command.split(' ', 1)
        self.w.rule(
                name,
                resource_filename('ninjaopenfoam', script) + ' ' + args,
                description=description,
                pool=pool)
        self.w.newline()
