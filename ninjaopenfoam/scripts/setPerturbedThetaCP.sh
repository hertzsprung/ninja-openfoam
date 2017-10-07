#!/bin/bash
set -e

display_usage() {
	echo -e <<EOF
Usage: setPerturbedThetaCP.sh <case>

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
mv $case/0/Tf $case/0/thetaf.perturbation

setTheta -case $case -CP
mv $case/0/theta $case/0/theta.background
mv $case/0/thetaf $case/0/thetaf.background

sumFields -case $case -scale0 1 -scale1 1 0 theta 0 theta.background 0 theta.perturbation
sumFields -case $case -scale0 1 -scale1 1 0 thetaf 0 thetaf.background 0 thetaf.perturbation
