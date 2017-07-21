#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: geodesicHexMesh.sh <case>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

case=$1

extrudeMesh -case $1
sed -i 's/patch/empty/g' $case/constant/polyMesh/boundary
sed -i -e '/sides/,+6d' $case/constant/polyMesh/boundary
sed -i '18s/3/2/' $case/constant/polyMesh/boundary
renumberMesh -case $case -constant -overwrite
