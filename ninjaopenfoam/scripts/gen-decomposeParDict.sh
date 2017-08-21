#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gen-decomposeParDict.sh <taskCount> <maxTaskCount>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

taskCount=$1
maxTaskCount=$2

export taskCount=$([ $taskCount -le $maxTaskCount ] && echo "$taskCount" || echo "$maxTaskCount")

envsubst <&0 >&1
