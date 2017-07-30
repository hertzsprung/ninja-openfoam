import os

class Paths:
    averageEquatorialSpacing = 'averageEquatorialSpacing.txt'
    courantNumber = 'co.txt'
    dx = 'dx.txt'
    mountainHeight = 'mountainHeight.txt'
    polyMesh = [os.path.join("constant/polyMesh", f) for f in ["points", "faces", "owner", "neighbour", "boundary"]]
    timestep = 'dt.txt'
