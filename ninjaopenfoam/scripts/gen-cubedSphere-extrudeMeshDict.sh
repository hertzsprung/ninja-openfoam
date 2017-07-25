#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gen-cubedSphere-extrudeMeshDict.sh <blockMeshCase>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

export blockMeshCase=$1

envsubst <&0 >&1
