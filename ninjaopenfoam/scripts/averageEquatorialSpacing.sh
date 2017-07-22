#!/bin/bash
set -e

python3 -c "import math; import sys; aveCellCentreDistance = float(sys.stdin.readline()); print(360*aveCellCentreDistance / (2*math.pi*6.3712e6))"
