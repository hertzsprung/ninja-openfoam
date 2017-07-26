import os

class Paths:
    averageEquatorialSpacing = 'averageEquatorialSpacing.txt'
    dx = 'dx.txt'
    polyMesh = [os.path.join("constant/polyMesh", f) for f in ["points", "faces", "owner", "neighbour", "boundary"]]

