class Rules:
    def write(self, generator):
        g = generator

        g.w.rule('blockMesh', 'blockMesh -case $case')
        g.w.newline()
        g.w.rule('cp', 'cp $in $out')
        g.w.newline()

        g.scriptRule(
                'averageCellCentreDistance',
                'scripts/averageCellCentreDistance.sh $case > $out',
                description='averageCellCentreDistance $case')

        g.scriptRule(
                'averageEquatorialSpacing',
                'scripts/averageEquatorialSpacing.sh < $in > $out',
                description='averageEquatorialSpacing $out')

        g.scriptRule(
                'collate',
                'scripts/collate.sh $independent $dependent $cases > $out',
                description='collate $out')

        g.scriptRule(
                'extractStat',
                'scripts/extractStat.sh $in $column > $out',
                description='extractStat $out')

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
                'globalSum',
                'scripts/globalSum.sh $case $time $field > $out',
                description='globalSum $out')

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
                'lperror',
                'scripts/lperror.sh $diff $analytic > $out',
                description='lperror $out')

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
                'sumFields',
                'scripts/sumFields.sh $case $analyticTime $analyticField $numericTime $numericField',
                description='sumFields $out')

        g.scriptRule(
                'terrainFollowingMesh',
                'scripts/terrainFollowingMesh.sh $blockMeshCase $terrainFollowingMeshCase',
                description='terrainFollowingMesh $terrainFollowingMeshCase')
