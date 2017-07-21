#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gnuplot.ninja.sh <in> <out>\n"
}

if [ $# -le 1 ]
then
	display_usage
	exit 1
fi

srcdir=$(dirname $1)
builddir=$(dirname $2)
document=$(basename $1 .tex)
gnuplot="gnuplot --persist"

set -a
source build.properties
$gnuplot -e "set output '$2'; set loadpath '$srcdir'; load '$1'"
