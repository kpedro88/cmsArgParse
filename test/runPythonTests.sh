#!/bin/sh

# Pass in name and status
function die { echo $1: status $2 ;  exit $2; }

for file in ${CMSSW_BASE}/src/FWCore/Args/python/*.py
do
  bn=`basename $file`
  if [ "$bn" != "__init__.py" ]; then
     bnm=${bn%.*} 
     python3 -m FWCore.Args."$bnm" || die "unit tests for $bn failed" $?
  fi
done

