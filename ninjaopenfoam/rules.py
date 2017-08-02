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
        
        g.w.rule(
                'courantNumber',
                "courantNumber -case $case | tail -n1 | cut -d' ' -f6 > $out",
                description='courantNumber $out')
        g.w.newline()

        g.scriptRule(
                'cubedSphereMesh',
                'scripts/cubedSphereMesh.sh $case $blockMeshCase',
                description='cubedSphereMesh $case')

        g.scriptRule(
                'cutCellMesh',
                'scripts/cutCellMesh.sh $case $patchSets',
                description='cutCellMesh $case')

        g.scriptRule(
                'cutCellPatch',
                'scripts/cutCellPatch.sh $case',
                description='cutCellPatch $case')

        g.w.rule('createSpongeLayer', 'createSpongeLayer -case $case')
        g.w.newline()

        g.w.rule('echo', 'echo $string > $out')
        g.w.newline()

        g.scriptRule(
                'extractStat',
                'scripts/extractStat.sh $in $column > $out',
                description='extractStat $out')

        g.scriptRule(
                'gen-cubedSphere-blockMeshDict',
                'scripts/gen-cubedSphere-blockMeshDict.sh $nxPerPatch < $in > $out',
                description='gen-cubedSphere-blockMeshDict $out')

        g.scriptRule(
                'gen-cubedSphere-extrudeMeshDict',
                'scripts/gen-cubedSphere-extrudeMeshDict.sh $blockMeshCase < $in > $out',
                description='gen-cubedSphere-extrudeMeshDict $out')

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
                'scripts/globalSum.sh $case $time $field',
                description='globalSum $out',
                pool='globalSum_pool')

        g.w.pool('globalSum_pool', 1)

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
                'gmtFoam-colorBar',
                'scripts/gmtFoam-colorBar.sh < $in > $out',
                description='gmtFoam-colorBar $out',
                pool='gmtFoam_pool')

        g.scriptRule(
                'latex-substitute',
                'scripts/latex-substitute.sh < $in > $out',
                description='latex-substitute $out')

        g.scriptRule(
                'lperror',
                'scripts/lperror.sh $diff $analytic > $out',
                description='lperror $out')

        g.w.rule(
                'maxw',
                "tr -s ' ' < $in | cut -d' ' -f6 | sort -g | tail -n1 > $out",
                description='maxw $out')
        g.w.newline()

        g.w.rule(
                'meanw',
                "tr -s ' ' < $in | cut -d' ' -f6 | tail -n +2 | datamash mean 1 > $out",
                description='maxw $out')
        g.w.newline()

        g.scriptRule(
                'pdflatex',
                'scripts/pdflatex.sh $in $out',
                description='pdflatex $in $out')

        g.scriptRule(
                's3-upload',
                'scripts/s3-upload.sh $source $s3uri > $out',
                description='s3upload $source')

        g.w.rule('setAnalyticTracerField', 'setAnalyticTracerField -case $case -time $time')
        g.w.newline()

        g.w.rule('setExnerBalancedH', 'setExnerBalancedH -case $case')
        g.w.newline()

        g.w.rule('setInitialTracerField', 'setInitialTracerField -case $case')
        g.w.newline()

        g.w.rule('setTheta', 'setTheta -case $case')
        g.w.newline()

        g.w.rule('setVelocityField', 'setVelocityField -case $case -time 0')
        g.w.newline()

        g.scriptRule(
                'siunitx-ang',
                'scripts/siunitx-ang.sh < $in > $out',
                description='siunitx-ang $out')

        g.scriptRule(
                'siunitx-num',
                'scripts/siunitx-num.sh < $in > $out',
                description='siunitx-num $out')

        g.scriptRule(
                'slantedCellMesh',
                'scripts/slantedCellMesh.sh $blockMeshCase $slantedCellMeshCase $removeTinyCells',
                description='slantedCellMesh $slantedCellMeshCase')

        g.scriptRule(
                'sumFields',
                'scripts/sumFields.sh $case $time $field',
                description='sumFields $out')

        g.scriptRule(
                'terrainFollowingMesh',
                'scripts/terrainFollowingMesh.sh $blockMeshCase $terrainFollowingMeshCase',
                description='terrainFollowingMesh $terrainFollowingMeshCase')
