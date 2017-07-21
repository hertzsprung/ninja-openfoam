#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: openfoam-solve.sh <case> <taskCount> <solver>\n"
}

if [ $# -lt 3 ]
then
	display_usage
	exit 1
fi

case=$1
taskCount=$2
solver=$3

decomposePar -force -constant -case $(realpath $case) # https://bugs.openfoam.org/view.php?id=2610
mpirun -np $taskCount $solver -parallel
reconstructPar -case $case
