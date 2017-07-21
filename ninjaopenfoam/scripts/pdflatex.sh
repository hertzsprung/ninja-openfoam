#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: pdflatex.ninja.sh <in> <out>\n"
}

if [ $# -le 1 ]
then
	display_usage
	exit 1
fi

srcdir=$(dirname $1)
builddir=$(dirname $2)
document=$(basename $1 .tex)
pdflatex="pdflatex -interaction=nonstopmode -halt-on-error -output-directory=$builddir"

$pdflatex -draft $1
openout_any=a bibtex $builddir/$document # https://tex.stackexchange.com/questions/223870/bibtex-error-not-writing-to-book-blg-openout-any-p-mactex-2014#comment525754_223870
$pdflatex -draft $1
$pdflatex $1
