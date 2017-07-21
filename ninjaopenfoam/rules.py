class Rules:
    def write(self, generator):
        g = generator

        g.w.rule('blockMesh', 'blockMesh -case $case')
        g.w.newline()
        g.w.rule('cp', 'cp $in $out')
        g.w.newline()

        g.scriptRule(
                'gen-controlDict',
                'scripts/gen-controlDict.sh $endTime $writeInterval $timestep < $in > $out',
                description='gen-controlDict $out')

        g.scriptRule(
                'gen-decomposeParDict',
                'scripts/gen-decomposeParDict.sh $solver_parallel_tasks < $in > $out',
                description='gen-decomposeParDict $out')

        g.scriptRule(
                'geodesicHexMesh',
                'scripts/geodesicHexMesh.sh $case',
                description='geodesicHexMesh $case')

        g.scriptRule(
                'geodesicHexPatch',
                'scripts/geodesicHexPatch.sh $case $refinement',
                description='geodesicHexPatch $case')

        g.scriptRule(
                'gnuplot',
                'scripts/gnuplot.sh $in $out',
                description='gnuplot $in $out')

        g.w.pool('gmtFoam_pool', 1)

        g.scriptRule(
                'gmtFoam',
                'scripts/gmtFoam.sh $in $case $time',
                description='gmtFoam $in $case $time',
                pool='gmtFoam_pool')

        g.scriptRule(
                'pdflatex',
                'scripts/pdflatex.sh $in $out',
                description='pdflatex $in $out')

        g.scriptRule(
                's3-upload',
                'scripts/s3-upload.sh $source $s3uri > $out',
                description='s3upload $source')

        g.w.rule('setInitialTracerField', 'setInitialTracerField -case $case')
        g.w.newline()
        g.w.rule('setVelocityField', 'setVelocityField -case $case -time 0')
        g.w.newline()

        g.scriptRule(
                'terrainFollowingMesh',
                'scripts/terrainFollowingMesh.sh $blockMeshCase $terrainFollowingMeshCase',
                description='terrainFollowingMesh $terrainFollowingMeshCase')
