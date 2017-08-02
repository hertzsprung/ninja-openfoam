import os

class Paths:
    averageEquatorialSpacing = 'averageEquatorialSpacing.txt'
    courantNumber = 'co.txt'
    dx = 'dx.txt'
    maxw = 'maxw.txt'
    meanw = 'meanw.txt'
    mountainHeight = 'mountainHeight.txt'
    polyMesh = [os.path.join("constant/polyMesh", f) for f in ["points", "faces", "owner", "neighbour", "boundary"]]
    timestep = 'dt.txt'
