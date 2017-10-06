#!/bin/bash
set -e

display_usage() {
	echo -e <<EOF
Usage: setPerturbedTheta.sh <case>

Create an initial theta field using setTheta and a perturbation provided by a tracerField.
EOF
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

export case=$1

setInitialTracerField -case $case
mv $case/0/T $case/0/theta.perturbation

setTheta -case $case
mv $case/0/theta $case/0/theta.bg

sumFields -case $case -scale0 1 -scale1 1 0 theta 0 theta.bg 0 theta.perturbation
