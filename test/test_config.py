import FWCore.ParameterSet.Config as cms
from FWCore.Args.cmsArgParse import cmsArgParse
import sys

parser = cmsArgParse(description='Test cmsArgParse')
parser.add_argument("--maxEvents", help="max events to process", type=int, default=1)
# same as a cmsRun argument
parser.add_argument("-n", "--numThreads", help="number of threads", type=int, default=1)
# same as an edmConfigDump argument
parser.add_argument("-o", "--output", help="output filename", type=str, default=None)
args = parser.parse_args()

process = cms.Process("TEST")
process.source = cms.Source("EmptySource")

process.maxEvents.input = args.maxEvents
process.options.numberOfThreads = args.numThreads
print("Output file: {}".format(args.output))
