#!/bin/bash
set -e

display_usage() {
	echo -e <<EOF
Usage: sumFields.sh <case> <time> <field>

Reads <time>/<field> and <time>/<field>_analytic, writes <time>/<field>_diff
EOF
}

if [ $# -lt 3 ]
then
	display_usage
	exit 1
fi

export case=$1
export time=$2
export field=$3

sumFields -case $case \
	$time ${field}_diff \
	$time $field \
	$time ${field}_analytic \
	-scale0 1 -scale1 -1 
