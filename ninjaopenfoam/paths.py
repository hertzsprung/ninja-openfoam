import os

class Paths:
    polyMesh = [os.path.join("constant", "polyMesh", f) for f in ["points", "faces", "owner", "neighbour", "boundary"]]

