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

decomposePar -force -time 0 -case $(realpath $case) # https://bugs.openfoam.org/view.php?id=2610

if [ -e $case/0/Uf ]; then
	for processorCase in $case/processor*; do
		fixProcessorFaceVelocities -case $processorCase
	done
fi

mpirun -np $taskCount $solver -parallel
reconstructPar -case $case
if [ -e $case/processor0/energy.dat ]; then
	cp $case/processor0/energy.dat $case/
fi
if [ -e $case/processor0/courant.dat ]; then
	cp $case/processor0/courant.dat $case/
fi
