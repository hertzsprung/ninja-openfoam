#!/bin/bash
out=$1; shift
> $out

while (( "$#" )); do
	points=$1
	cpu_file=$2
	echo -n "$points " | cat - $cpu_file >> $out
	shift 2
done
