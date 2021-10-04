#!/bin/bash

IN_NAME=$1
IN_PDS=$2

cp ${IN_NAME}.ofcob ${IN_NAME}.so
dlupdate ${PWD}/${IN_NAME}.so $IN_PDS