#!/bin/bash

for region in `ls ${OPENFRAME_HOME}/config/*osc_* | awk -F"[_.]" '{print $3}'`
  cp ${1}.phm /opt/tmaxapp/OpenFrame/osc/region/${item}/map/physical
  cp ${1}.cpy /opt/tmaxapp/OpenFrame/osc/region/${item}/map/symbolic
done