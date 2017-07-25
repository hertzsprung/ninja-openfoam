#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: cubedSphereMesh.sh <case> <blockMeshCase>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

case=$1
blockMeshCase=$2

tanPoints -case $blockMeshCase
extrudeMesh -case $case
sed -i 's/patch/empty/g' $case/constant/polyMesh/boundary
