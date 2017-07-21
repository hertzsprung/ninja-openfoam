#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: gmtFoam.ninja.sh <gmtDict> <case> <time>\n"
}

if [ $# -le 2 ]
then
	display_usage
	exit 1
fi

gmtDict=$(basename $1)
ofCase=$2

if [ $3 = "constant" ]
then
	ofTime=-constant
else
	ofTime="-time $3"
fi

gmtFoam -case $ofCase $ofTime $gmtDict
