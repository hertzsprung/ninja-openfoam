#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gen-decomposeParDict.sh <taskCount>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

export taskCount=$1

envsubst <&0 >&1
