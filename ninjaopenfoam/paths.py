import os

class Paths:
    averageEquatorialSpacing = 'averageEquatorialSpacing.txt'
    polyMesh = [os.path.join("constant/polyMesh", f) for f in ["points", "faces", "owner", "neighbour", "boundary"]]

