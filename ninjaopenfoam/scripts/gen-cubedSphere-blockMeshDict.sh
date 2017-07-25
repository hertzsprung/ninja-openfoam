#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gen-cubedSphere-blockMeshDict.sh <nxPerPatch>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

export nxPerPatch=$1

envsubst <&0 >&1
