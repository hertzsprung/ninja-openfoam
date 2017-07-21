import errno
import os

from .generator import Generator
from .rules import Rules
from pkg_resources import resource_filename

class Build:
    def __init__(self):
        self.gendir = 'build.ninja.generated'
        self.cases = []

    def add(self, case):
        self.cases.append(case)

    def write(self):
        self.makegendir()

        with open('{gendir}/rules.ninja'.format(gendir=self.gendir), 'wt') as out:
            g = Generator(out)
            g.header()

            Rules().write(g)

        with open('build.ninja', 'wt') as out:
            g = Generator(out)
            g.header()

            g.w.variable('builddir', 'build')
            g.w.variable('gendir', self.gendir)

            g.w.rule('generate', command='./generate.py', generator=True)
            g.w.build('build.ninja', 'generate', implicit='generate.py')

            g.w.include('build.properties')
            g.w.include('$gendir/rules.ninja')#resource_filename('ninjaopenfoam', 'data/rules.ninja'))

            for case in self.cases:
                g.w.include('$gendir/{case}.build.ninja'.format(case=case))

        for case in self.cases:
            with open(
                    '{gendir}/{case}.build.ninja'.format(
                        gendir=self.gendir, case=case),
                    'wt') as out:
                g = Generator(out)
                g.header()

                case.write(g)

    def makegendir(self):
        try:
            os.makedirs(self.gendir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise