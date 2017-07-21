import os

class Shortcuts:
    def __init__(self, inputs):
        self.shortcuts = [(i, os.path.basename(i)) for i in inputs]

    def write(self, generator):
        for target, link in self.shortcuts:
            generator.w.build(link, 'cp', target)

    def __str__(self):
        return 'shortcuts'
