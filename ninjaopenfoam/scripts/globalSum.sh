#!/bin/bash
set -e

display_usage() {
	echo -e <<EOF
Usage: globalSum.sh <case> <time> <field>

Reads <time>/<field>, writes <time>/globalSum<field>.dat
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

globalSum -case $case -time $time $field
mv $case/globalSum$field.dat $case/$time/globalSum$field.dat
