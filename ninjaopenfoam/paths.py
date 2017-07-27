import os

class Paths:
    averageEquatorialSpacing = 'averageEquatorialSpacing.txt'
    dx = 'dx.txt'
    mountainHeight = 'mountainHeight.txt'
    polyMesh = [os.path.join("constant/polyMesh", f) for f in ["points", "faces", "owner", "neighbour", "boundary"]]

