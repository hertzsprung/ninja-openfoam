class SolverRule:
    def __init__(self, name, command, parallel):
        self.name = name
        self.command = command
        self.parallel = parallel

    def write(self, generator):
        g = generator

        description = "{name} $case".format(name=self.name)

        if self.parallel:
            g.scriptRule(
                    self.name,
                    'scripts/openfoam-solve.sh $case $solver_parallel_tasks "{command} -parallel"'.format(command=self.command),
                    description=description)
        else:
            g.w.rule(self.name, self.command, description=description)

    def __str__(self):
        return self.name

class SolverExecution:
    def __init__(self, generator, case, parallel=False, decomposeParDict=None):
        self.g = generator
        self.case = case
        self.parallel = parallel
        self.decomposeParDict = decomposeParDict

    def solve(self, outputs, rule, inputs=None, implicit=[], order_only=None,
              variables={}, implicit_outputs=None):
        implicit += self.case.polyMesh + self.case.systemFiles
        if self.parallel:
            implicit += [self.case.decomposeParDict]

        variables["case"] = self.case
        variables["pool"] = "console"

        self.g.w.build(outputs, rule, inputs, implicit, order_only, 
                variables, implicit_outputs)
        self.g.w.newline() 

        if self.parallel:
            self.g.w.build(
                    outputs=self.case.decomposeParDict,
                    rule="gen-decomposeParDict",
                    inputs=self.decomposeParDict
            )
            self.g.w.newline() 

