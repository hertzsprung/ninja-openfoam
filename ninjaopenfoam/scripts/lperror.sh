#!/bin/bash
set -e

display_usage() {
	echo -e "Usage: lperror.sh <diff> <analytic>\n"
}

if [ $# -lt 2 ]
then
	display_usage
	exit 1
fi

export diff=$1
export analytic=$2

python3 -c "print(`paste -d'/' $diff $analytic`)"

