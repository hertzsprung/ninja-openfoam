#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: cutCellMesh.sh <case> <patchSets>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

case=$1
patchSets=$2

extrudeMesh -case $case
setSet -case $1 -constant -noVTK -batch $patchSets
createPatch -case $1 -overwrite
