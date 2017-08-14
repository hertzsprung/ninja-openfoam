#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: pdflatex-figure.sh <in> <out>\n"
}

if [ $# -le 1 ]
then
	display_usage
	exit 1
fi

builddir=$(dirname $2)
pdflatex="pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$builddir"

$pdflatex $1
