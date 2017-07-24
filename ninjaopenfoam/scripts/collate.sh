#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: collate.sh <independent> <dependent> <cases...>\n"
}

if [ $# -lt 3 ]
then
	display_usage
	exit 1
fi

export independent=$1
export dependent=$2
export cases="${@:3}"

for case in $cases; do
	paste -d' ' $case/$independent $case/$dependent
done

