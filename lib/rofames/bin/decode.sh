#!/bin/bash

JAVA_HOME_BIN=$1
XP_DIR=$2
tagger=$3
max_ram=$4
use_hierarchy=$5
LOGS_DIR=$6

if [ "${use_hierarchy}" = FALSE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0.jar"
fi

if [ "${use_hierarchy}" = TRUE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0-hier.jar"
fi

echo "ROFAMES TRAIN MODE OPTIONS"
echo "  JAVA_HOME_BIN = ${JAVA_HOME_BIN}"
echo "  CLASSPATH = ${CLASSPATH}"
echo "  XP_DIR = ${XP_DIR}"
echo "  tagger = ${tagger}"
echo "  max_ram = ${max_ram}"
echo "  use_hierarchy = ${use_hierarchy}"
echo "  LOGS_DIR = ${LOGS_DIR}"
echo

echo "Decoding with ROFAMES..."
${JAVA_HOME_BIN}/java \
    -classpath ${CLASSPATH} \
    -Xmx${max_ram} \
    edu.unige.clcl.fn.score.ScoreWithFrames \
    ${XP_DIR}/data/test.sentences.${tagger}.conllx \
    ${XP_DIR}/data/test.frames \
    ${XP_DIR}/model/parser.conf \
    ${XP_DIR}/data/framenet.frame.element.map \
    ${XP_DIR}/model/argmodel.dat \
    1 \
    ${XP_DIR}/data/test.frame.elements > ${LOGS_DIR}/rofames.decode.log
