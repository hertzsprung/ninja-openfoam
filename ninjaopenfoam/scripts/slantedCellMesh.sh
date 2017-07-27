#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: slantedCellMesh.ninja.sh <blockMeshCase> <slantedCellMeshCase> <removeTinyCells>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

blockMeshCase=$1
case=$2
removeTinyCells=$3

mkdir -p $case/constant
cp -r $blockMeshCase/constant/polyMesh $case/constant
slantMesh -case $case
checkCellVolumes -case $case
setSet -case $case -constant -noVTK -batch $removeTinyCells
subsetMesh -case $case -patch ground -overwrite bigCells
rm -rf $case/constant/polyMesh/sets/bigCells $case/constant/polyMesh/sets/tinyCells
checkMesh -case $case -constant
if [ -e $case/constant/polyMesh/sets/wrongOrientedFaces ]; then
	collapseEdges -case $case -constant -overwrite
fi
checkMesh -case $case -constant
if [ -e $1/constant/polyMesh/sets/zeroAreaFaces ]; then
	collapseEdges -case $case -constant -overwrite -collapseFaceSet zeroAreaFaces
fi
