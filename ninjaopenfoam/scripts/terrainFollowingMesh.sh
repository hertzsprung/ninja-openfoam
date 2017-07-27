#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: terrainFollowingMesh.sh <blockMeshCase> <terrainFollowingMeshCase>\n"
}

if [ $# -le 1 ]
then
	display_usage
	exit 1
fi

blockMeshCase=$1
terrainFollowingMeshCase=$2

mkdir -p $terrainFollowingMeshCase/constant
cp -r $blockMeshCase/constant/polyMesh $terrainFollowingMeshCase/constant
terrainFollowingMesh -case $terrainFollowingMeshCase
