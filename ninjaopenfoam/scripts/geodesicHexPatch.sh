#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: geodesicHexPatch.sh <case> <refinement>\n"
}

if [ $# -le 1 ]
then
	display_usage
	exit 1
fi

case=$1
refinement=$2

cd $case
gengrid_hex.$refinement
