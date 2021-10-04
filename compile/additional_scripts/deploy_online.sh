#!/bin/bash

IN_NAME=$1

cp ${IN_NAME}.ofcob ${IN_NAME}.so

for region in `ls ${OPENFRAME_HOME}/config/*osc_* | awk -F"[_.]" '{print $3}'`
 do
  install ${IN_NAME}.so  ${OPENFRAME_HOME}/osc/region/${region}/tdl/mod
#  osctdlupdate $region $IN_NAME

done
#exit 0
