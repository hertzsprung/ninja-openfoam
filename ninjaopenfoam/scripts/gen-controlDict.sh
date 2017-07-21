#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gen-controlDict.sh <endTime> <writeInterval> <timestep>\n"
}

if [ $# -lt 3 ]
then
	display_usage
	exit 1
fi

export endTime=$1
export writeInterval=$2
export timestep=$3

envsubst <&0 >&1
