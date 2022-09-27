#Time to create the trees, that is the input the resolution plots script
thedate="20220923"
#Change this to your personal folder of preference
outputarea="/eos/user/c/chtee/CalibrationStudies"
#In this example we shoot to the CE_E_Front_120um
region="CE_E_Front_120um"
#In the for loop below we will create two folders. The Ntuples_${thedate}
#will contain the merged ntuples from the RECO step per region, while the ResolutionTrees_${thedate}
#will contain the trees to fit for the resolution plot. 
#This dirs variable points to the folders with the output ntuples of the RECO step. We want to 
#merge these output files and gather them in a dedicated folder, that is the Ntuples_${thedate}. 
dirs=`ls -d /eos/user/c/chtee/CalibrationStudies/CloseByParticleGunProducer_chtee_*${region}*chtee*${thedate}/RECO`
for i in $region; do echo $i; mkdir -p ${outputarea}/Ntuples_${thedate}/${region}; mkdir -p ${outputarea}/ResolutionTrees_${thedate}/${region}; for j in $dirs; do echo ${j}; mergename=`ls ${j}/*hgc_1.root | awk -F"RECO/" '{print $2}' | awk -F"_1.root" '{print $1}'`; echo $mergename; hadd ${outputarea}/Ntuples_${thedate}/${region}/${mergename}.root ${j}/*hgc*.root;done; done;


recotrees=`ls ${outputarea}/Ntuples_${thedate}/${region}`
soncut="3"
for i in $recotrees; do echo $i; energy=`echo $i | awk -F"_E" '{print $2}' | awk -F".0To" '{print $1}'`; echo $energy; mkdir -p simclusters_singlephoton_e${energy}GeV_${region}; time python3 /afs/cern.ch/user/c/chtee/HGCAL_production/CMSSW_12_3_0_pre6/src/HGCalValidator/HGCalAnalysis/python/monitorHGCAL.py --input ${outputarea}/Ntuples_${thedate}/${region}/${i} --object SimClusters --maxEvents 1000 --verbosityLevel 2 --output hgc_singlephoton_e${energy}GeV_nopu --outDir simclusters_singlephoton_e${energy}GeV_${region} --ecut ${soncut} --genEnergy ${energy}; cp simclusters_singlephoton_e${energy}GeV_${region}/hgc_singlephoton_e${energy}GeV_nopu.root ${outputarea}/ResolutionTrees_${thedate}/${region}/. ; done;