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
                'ghostMesh',
                'scripts/ghostMesh.sh $case',
                description='ghostMesh $case')

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
                'maxKE',
                "tr -s ' ' < $in | cut -d' ' -f2 | sort -g | tail -n1 > $out",
                description='maxKE $out')
        g.w.newline()

        g.scriptRule(
                'pdflatex',
                'scripts/pdflatex.sh $in $out',
                description='pdflatex $out')

        g.scriptRule(
                'pdflatex-figure',
                'scripts/pdflatex-figure.sh $in $out',
                description='pdflatex-figure $out')

        g.w.rule('pysgswe-intrusive',
                'pysgswe-intrusive $root $testcase $basis --max-basis $max_basis --basis-dimensions $basis_dimensions $truncate_basis $end_time $elements',
                description='pysgswe-intrusive $root')

        g.w.rule('pysgswe-intrusive-sample-quadrature-points',
                'pysgswe-intrusive $root $testcase $basis --max-basis $max_basis --basis-dimensions $basis_dimensions $truncate_basis $end_time $elements --response-curves $sample_indices',
                description='pysgswe-intrusive $root')

        g.w.rule('pysgswe-intrusive-sample-smooth-points',
                'pysgswe-intrusive $root $testcase $basis --max-basis $max_basis --basis-dimensions $basis_dimensions $truncate_basis $end_time $elements --response-curves $sample_indices --sample-points $sample_points',
                description='pysgswe-intrusive $root')

        g.w.rule('pysgswe-nonintrusive',
                'pysgswe-nonintrusive $root --max-level $max_level',
                description='pysgswe-nonintrusive $root')

        g.w.rule('pysgswe-nonintrusive-sample-uniform',
                'pysgswe-nonintrusive $root --sample-uniform $sample_uniform',
                description='pysgswe-nonintrusive $root')

        g.scriptRule(
                's3-upload',
                'scripts/s3-upload.sh $source $s3uri > $out',
                description='s3upload $source')

        g.w.rule('sample', 'postProcess -case $case -time $time -func sampleDict')
        g.w.newline()

        g.w.rule('scalarDeformationHighOrderFit', 'scalarDeformationHighOrderFit -case $case', pool='console')
        g.w.newline()

        g.w.rule('scalarDeformation', 'scalarDeformation -case $case', pool='console')
        g.w.newline()

        g.w.rule('setAnalyticTracerField', 'setAnalyticTracerField -case $case -time $time')
        g.w.newline()

        g.w.rule('setExnerBalancedH', 'setExnerBalancedH -case $case')
        g.w.newline()

        g.w.rule('setExnerBalancedCP', 'setExnerBalancedH -case $case -noInterpolate')
        g.w.newline()

        g.w.rule('setGaussians', 'setGaussians -case $case setGaussiansDict')
        g.w.newline()

        g.w.rule('setInitialTracerField', 'setInitialTracerField -case $case')
        g.w.newline()

        g.w.rule('setTheta', 'setTheta -case $case')
        g.w.newline()

        g.w.rule('setThetaCP', 'setTheta -case $case -CP')
        g.w.newline()

        g.scriptRule(
                'setPerturbedTheta',
                'scripts/setPerturbedTheta.sh $case',
                description='setPerturbedTheta $case')

        g.scriptRule(
                'setPerturbedThetaCP',
                'scripts/setPerturbedThetaCP.sh $case',
                description='setPerturbedThetaCP $case')

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
                'siunitx-timestep',
                'scripts/siunitx-timestep.sh < $in > $out',
                description='siunitx-timestep $out')

        g.scriptRule(
                'siunitx-velocity',
                'scripts/siunitx-velocity.sh < $in > $out',
                description='siunitx-velocity $out')

        g.scriptRule(
                'slantedCellMesh',
                'scripts/slantedCellMesh.sh $blockMeshCase $slantedCellMeshCase $removeTinyCells',
                description='slantedCellMesh $slantedCellMeshCase')

        g.scriptRule(
                'sumFields',
                'scripts/sumFields.sh $case $time $field',
                description='sumFields $out')

        g.scriptRule(
                'swepc',
                'scripts/swepc.sh $outputDir $testCase $solver $degree $elements $endTime $dt $topographyMean',
                description='swepc $out')

        g.scriptRule(
                'swepdf',
                'scripts/swepdf.sh $in $variable $min $max $samples $line > $out',
                description='swepc $out')

        g.scriptRule(
                'swemc',
                'scripts/swemc.sh $outputDir $testCase $solver $iterations $sampleIndex $elements $endTime $dt',
                description='swemc $out')

        g.scriptRule(
                'terrainFollowingMesh',
                'scripts/terrainFollowingMesh.sh $blockMeshCase $terrainFollowingMeshCase',
                description='terrainFollowingMesh $terrainFollowingMeshCase')
