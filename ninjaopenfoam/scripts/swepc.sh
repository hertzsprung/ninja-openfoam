#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: swepc.sh <testCase> <solver> <degree> <elements> <endTime> <dt>\n"
}

if [ $# -lt 6 ]
then
	display_usage
	exit 1
fi

export testCase=$1
export solver=$2
export degree=$3
export elements=$4
export endTime=$5
export dt=$6

swepc $testCase $solver -d $degree -M $elements --end-time $endTime --dt $dt
