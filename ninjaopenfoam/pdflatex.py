import os

class PDFLaTeX:
    def __init__(self, name, output, document, components=[]):
        self.name = name
        self.output = os.path.join('$builddir', output + '.pdf')
        self.document = document + '.tex'
        self.components = components

    def write(self, generator):
        generator.w.build(
           self.output,
           'pdflatex',
            self.document,
            implicit=self.components)

    def __str__(self):
        return self.name
