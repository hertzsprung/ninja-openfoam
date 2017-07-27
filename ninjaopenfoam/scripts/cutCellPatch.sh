#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: cutCellPatch.sh <case>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

case=$1

(cd $case && GridGen asam.grid)
gmvread $case/asam.out.gmvG $case
gmv2obj $case $case/vertical_slice.obj

