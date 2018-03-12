#!/bin/bash

JAVA_HOME_BIN=$1
XP_DIR=$2
splits=$3
kbest=$4
max_ram=$5
with_hierarchy=$6
LOGS_DIR=$7

if [ "${with_hierarchy}" = TRUE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0-hier.jar"
  echo "ROFAMES TRAIN MODE OPTIONS"
  echo "  JAVA_HOME_BIN = ${JAVA_HOME_BIN}"
  echo "  CLASSPATH = ${CLASSPATH}"
  echo "  XP_DIR = ${XP_DIR}"
  echo "  splits = ${splits}"
  echo "  kbest = ${kbest}"
  echo "  max_ram = ${max_ram}"
  echo "  with_hierarchy = ${with_hierarchy}"
  echo "  LOGS_DIR = ${LOGS_DIR}"
  echo

  echo "Decoding with ROFAMES..."
  ${JAVA_HOME_BIN}/java \
      -classpath ${CLASSPATH} \
      -Xmx${max_ram} \
      edu.unige.clcl.fn.score.ScoreWithFrames \
      ${XP_DIR}/data/${splits}.sentences.conllx \
      ${XP_DIR}/data/${splits}.frames \
      ${XP_DIR}/model/parser.conf \
      ${XP_DIR}/data/framenet.frame.element.map \
      ${XP_DIR}/model/argmodel.dat \
      ${kbest} \
      ${XP_DIR}/data/${splits}.frame.elements \
      ancestors_file:${XP_DIR}/data/ancestors.csv \
      frame_parents_file:${XP_DIR}/data/frame_parents.csv \
      frame_parent_rolemappings_file:${XP_DIR}/data/frame_parent_rolemappings.csv
fi

if [ "${with_hierarchy}" = FALSE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0.jar"
  echo "ROFAMES TRAIN MODE OPTIONS"
  echo "  JAVA_HOME_BIN = ${JAVA_HOME_BIN}"
  echo "  CLASSPATH = ${CLASSPATH}"
  echo "  XP_DIR = ${XP_DIR}"
  echo "  splits = ${splits}"
  echo "  kbest = ${kbest}"
  echo "  max_ram = ${max_ram}"
  echo "  with_hierarchy = ${with_hierarchy}"
  echo "  LOGS_DIR = ${LOGS_DIR}"
  echo

  echo "Decoding with ROFAMES..."
  ${JAVA_HOME_BIN}/java \
      -classpath ${CLASSPATH} \
      -Xmx${max_ram} \
      edu.unige.clcl.fn.score.ScoreWithFrames \
      ${XP_DIR}/data/${splits}.sentences.conllx \
      ${XP_DIR}/data/${splits}.frames \
      ${XP_DIR}/model/parser.conf \
      ${XP_DIR}/data/framenet.frame.element.map \
      ${XP_DIR}/model/argmodel.dat \
      ${kbest} \
      ${XP_DIR}/data/${splits}.frame.elements
fi
