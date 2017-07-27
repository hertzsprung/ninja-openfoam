#!/bin/bash
set -e
set -a
source build.properties

envsubst | python3 -c"
import re
import sys

f = sys.stdin.read()

def input_replace(match):
    with open(match.group(1), 'r') as replacement:
        return replacement.read()

print(re.sub(r'\\\\input{(.+?)}', input_replace, f))
"
