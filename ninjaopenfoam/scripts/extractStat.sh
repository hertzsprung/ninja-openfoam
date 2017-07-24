#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: extractStat.sh <globalSum.dat> <column-index>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

export file=$1
export column=$2

tail -n1 $file | cut -d' ' -f$column
