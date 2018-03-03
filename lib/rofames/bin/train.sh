#!/bin/bash

JAVA_HOME_BIN=$1
XP_DIR=$2
lambda=$3
kbest=$4
batch_size=$5
save_every_k_batches=$6
num_models_to_save=$7
min_ram=$8
max_ram=$9
num_threads=${10}
with_hierarchy=${11}
LOGS_DIR=${12}

if [ "${with_hierarchy}" = FALSE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0.jar"
fi

if [ "${with_hierarchy}" = TRUE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0-hier.jar"
fi

echo "ROFAMES TRAIN MODE OPTIONS"
echo "  JAVA_HOME_BIN = ${JAVA_HOME_BIN}"
echo "  CLASSPATH = ${CLASSPATH}"
echo "  XP_DIR = ${XP_DIR}"
echo "  lambda = ${lambda}"
echo "  kbest = ${kbest}"
echo "  batch_size = ${batch_size}"
echo "  save_every_k_batches = ${save_every_k_batches}"
echo "  num_models_to_save = ${num_models_to_save}"
echo "  min_ram = ${min_ram}"
echo "  max_ram = ${max_ram}"
echo "  num_threads = ${num_threads}"
echo "  with_hierarchy = ${with_hierarchy}"
echo "  LOGS_DIR = ${LOGS_DIR}"
echo

mkdir ${XP_DIR}/model 2> /dev/null

echo "Training ROFAMES..."

echo
echo "Argument Identification -- Step 1: Creating alphabet"
echo
${JAVA_HOME_BIN}/java \
    -classpath ${CLASSPATH} \
    -Xms${min_ram} \
    -Xmx${max_ram} \
    edu.cmu.cs.lti.ark.fn.parsing.CreateAlphabet \
    ${XP_DIR}/data/train.frame.elements \
    ${XP_DIR}/data/train.sentences.conllx.flattened \
    ${XP_DIR}/model/train.events.bin \
    ${XP_DIR}/model/parser.conf \
    ${XP_DIR}/model/train.sentences.frame.elements.spans \
    true \
    ${kbest} \
    null > ${LOGS_DIR}/rofames.train.create.alphabet.log

echo
echo "Argument Identification -- Step 2: Caching feature vectors"
echo
${JAVA_HOME_BIN}/java \
    -classpath ${CLASSPATH} \
    -Xms${min_ram} \
    -Xmx${max_ram} \
    edu.cmu.cs.lti.ark.fn.parsing.CacheFrameFeaturesApp \
    events_file:${XP_DIR}/model/train.events.bin \
    spans_file:${XP_DIR}/model/train.sentences.frame.elements.spans \
    train_frame_file:${XP_DIR}/data/train.frame.elements \
    local_features_cache:${XP_DIR}/model/featurecache.jobj > ${LOGS_DIR}/rofames.train.cache.feature.vectors.log


echo
echo "Argument identification -- Step 3: Training argument identification model"
echo
${JAVA_HOME_BIN}/java \
    -classpath ${CLASSPATH} \
    -Xms${min_ram} \
    -Xmx${max_ram} \
    edu.cmu.cs.lti.ark.fn.parsing.TrainArgIdApp \
    model:${XP_DIR}/model/argmodel.dat \
    alphabet_file:${XP_DIR}/model/parser.conf \
    local_features_cache:${XP_DIR}/model/featurecache.jobj \
    lambda:${lambda} \
    num_threads:${num_threads} \
    batch_size:${batch_size} \
    save_every_k_batches:${save_every_k_batches} \
    num_models_to_save:${num_models_to_save} > ${LOGS_DIR}/rofames.train.model.log

# get the last model file created
model_file="$(ls ${XP_DIR}/model/argmodel.dat_* | sort -r | head -n1)"
echo "Using model file: ${model_file}"
echo
cp ${model_file} ${XP_DIR}/model/argmodel.dat
rm ${XP_DIR}/model/argmodel.dat_*
