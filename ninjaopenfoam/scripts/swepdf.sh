#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: swepdf.sh <coefficientsFile> <variable> <min> <max> <samples> <line>\n"
}

if [ $# -lt 6 ]
then
	display_usage
	exit 1
fi

export coefficientsFile=$1
export variable=$2
export min=$3
export max=$4
export samples=$5
export line=$6

sed -n ${line}p $coefficientsFile | swepdf --min $min --max $max --samples $samples $variable

