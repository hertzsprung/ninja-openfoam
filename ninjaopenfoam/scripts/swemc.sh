#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: swemc.sh <outputDir> <testCase> <solver> <iterations> <sampleIndex> <elements> <endTime> <dt>\n"
}

if [ $# -lt 8 ]
then
	display_usage
	exit 1
fi

export outputDir=$1
export testCase=$2
export solver=$3
export iterations=$4
export sampleIndex=$5
export elements=$6
export endTime=$7
export dt=$8

swepc --monte-carlo --mc-iterations $iterations --mc-sample-index $sampleIndex $testCase $solver -M $elements --end-time $endTime --dt $dt -o $outputDir

