import FWCore.ParameterSet.Config as cms

from HGCalValidator.HGCalProduction.GSD_fragment import process

process.maxEvents.input = cms.untracked.int32(1000)

# random seeds
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(4)
process.RandomNumberGeneratorService.VtxSmeared.initialSeed = cms.untracked.uint32(4)
process.RandomNumberGeneratorService.mix.initialSeed = cms.untracked.uint32(4)

# Input source
process.source.firstLuminosityBlock = cms.untracked.uint32(4)

# Output definition
process.FEVTDEBUGHLToutput.fileName = cms.untracked.string('file:closeby_PDGid11_x1000_E100.0To100.0_GSD_4.root')

#DUMMYPUSECTION

gunmode = 'closeby'

if gunmode == 'default':
    process.generator = cms.EDProducer("CloseByParticleGunProducer",
        AddAntiParticle = cms.bool(True),
        PGunParameters = cms.PSet(
            MaxEta = cms.double(4.0),
            MaxPhi = cms.double(3.14159265359),
            MaxE = cms.double(100.0),
            MinEta = cms.double(1.4),
            MinPhi = cms.double(-3.14159265359),
            MinE = cms.double(100.0),
            #DUMMYINCONESECTION
            PartID = cms.vint32(11)
        ),
        Verbosity = cms.untracked.int32(0),
        firstRun = cms.untracked.uint32(1),
        psethack = cms.string('multiple particles predefined pT/E eta 1p479 to 3')
    )
elif gunmode == 'pythia8':
    process.generator = cms.EDFilter("CloseByParticleGunProducer",
        maxEventsToPrint = cms.untracked.int32(1),
        pythiaPylistVerbosity = cms.untracked.int32(1),
        pythiaHepMCVerbosity = cms.untracked.bool(True),
        PGunParameters = cms.PSet(
          ParticleID = cms.vint32(11),
          AddAntiParticle = cms.bool(True),
          MinPhi = cms.double(-3.14159265359),
          MaxPhi = cms.double(3.14159265359),
          MinE = cms.double(100.0),
          MaxE = cms.double(100.0),
          MinEta = cms.double(1.4),
          MaxEta = cms.double(4.0)
          ),
        PythiaParameters = cms.PSet(parameterSets = cms.vstring())
    )
elif gunmode == 'closeby':
    process.generator = cms.EDProducer("CloseByParticleGunProducer",
        AddAntiParticle = cms.bool(False),
        PGunParameters = cms.PSet(
            ControlledByEta = cms.bool(False),
            PartID = cms.vint32(11),
            EnMin = cms.double(100.0),
            EnMax = cms.double(100.0),
            MaxEnSpread = cms.bool(False),
            RMin = cms.double(54.99),
            RMax = cms.double(55.01),
            ZMin = cms.double(320.99),
            ZMax = cms.double(321.01),
            Delta = cms.double(2.5),
            Pointing = cms.bool(True),
            Overlapping = cms.bool(False),
            RandomShoot = cms.bool(False),
            NParticles = cms.int32(1),
            MaxEta = cms.double(4.0),
            MinEta = cms.double(1.4),
            MaxPhi = cms.double(3.14159265359),
            MinPhi = cms.double(-3.14159265359)
        ),
        Verbosity = cms.untracked.int32(10),
        psethack = cms.string('single or multiple particles predefined E moving vertex'),
        firstRun = cms.untracked.uint32(1)
    )
elif gunmode == 'physproc':

    # CloseByParticleGunProducer is a string in the form of proc[:jetColl:threshold:min_jets]
    physicsProcess = 'CloseByParticleGunProducer'
    proc_cfg = physicsProcess.split(':')
    proc = proc_cfg[0]

    # phase space cuts
    ptMin = 100.0
    ptMax = 100.0

    from reco_prodtools.templates.hgcBiasedGenProcesses_cfi import *

    #define the process
    #print 'Setting process to', proc
    defineProcessGenerator(process, proc=proc, ptMin=ptMin, ptMax=ptMax)

    #set a filter path if it's available
    if len(proc_cfg)==4:
        jetColl = proc_cfg[1]
        thr = float(proc_cfg[2])
        minObj = int(proc_cfg[3])
        #print 'Adding a filter with the following settings:'
        #print '\tgen-jet collection for filtering:', jetColl
        #print '\tpT threshold [GeV]:', thr
        #print '\tmin. number of jets with the above threshold:', minObj
        filterPath = defineJetBasedBias(process, jetColl=jetColl, thr=thr, minObj=minObj)
        process.schedule.extend([filterPath])
        process.FEVTDEBUGHLToutput.SelectEvents.SelectEvents=cms.vstring(filterPath.label())
