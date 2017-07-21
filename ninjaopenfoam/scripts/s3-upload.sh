#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: s3-upload.sh <source> <s3uri>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

source=$1
target=$2

aws s3 cp --recursive --exclude 'processor*' $source $target$(basename $source)
