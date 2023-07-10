import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
import sys

options = VarParsing("analysis")
options.register("threads", 1, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("output", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.parseArguments()

process = cms.Process("TEST")
process.source = cms.Source("EmptySource")

process.maxEvents.input = options.maxEvents
process.options.numberOfThreads = options.threads
print("Output file: {}".format(options.output))
