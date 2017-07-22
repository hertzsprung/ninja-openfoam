#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: averageCellCentreDistance.sh <case>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

case=$1

cellCentreDistances -case $case | tail -n +26 | datamash mean 1
