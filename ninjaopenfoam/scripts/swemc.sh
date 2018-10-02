#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: swemc.sh <testCase> <solver> <iterations> <sampleIndex> <elements> <endTime> <dt>\n"
}

if [ $# -lt 6 ]
then
	display_usage
	exit 1
fi

export testCase=$1
export solver=$2
export iterations=$3
export sampleIndex=$4
export elements=$5
export endTime=$6
export dt=$7

swepc --monte-carlo --mc-iterations $iterations --mc-sample-index $sampleIndex $testCase $solver -M $elements --end-time $endTime --dt $dt

