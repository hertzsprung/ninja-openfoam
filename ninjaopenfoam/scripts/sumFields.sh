#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: sumFields.sh <case> <analyticTime> <analyticField> <numericTime> <numericField>\n"
}

if [ $# -lt 5 ]
then
	display_usage
	exit 1
fi

export case=$1
export analyticTime=$2
export analyticField=$3
export numericTime=$4
export numericField=$5

sumFields -case $case \
	$numericTime ${numericField}_diff \
	$numericTime $numericField \
	$analyticTime $analyticField \
	-scale0 1 -scale1 -1 
