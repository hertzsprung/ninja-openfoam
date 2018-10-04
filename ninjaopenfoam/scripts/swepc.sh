#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: swepc.sh <outputDir> <testCase> <solver> <degree> <elements> <endTime> <dt>\n"
}

if [ $# -lt 7 ]
then
	display_usage
	exit 1
fi

export outputDir=$1
export testCase=$2
export solver=$3
export degree=$4
export elements=$5
export endTime=$6
export dt=$7

swepc $testCase $solver -d $degree -M $elements --end-time $endTime --dt $dt -o $outputDir
