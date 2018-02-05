set -e

display_usage() {
	echo -e "Usage: ghostMesh.sh <case>\n"
}

if [ $# -lt 1 ]
then
	display_usage
	exit 1
fi

case=$1

blockMesh -case $case
createGhostMesh -case $case 3
stitchMesh -case $case -perfect -overwrite -region ghostMesh inlet outlet2
stitchMesh -case $case -perfect -overwrite -region ghostMesh outlet inlet1
