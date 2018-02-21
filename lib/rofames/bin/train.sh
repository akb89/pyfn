#!/bin/bash

JAVA_HOME_BIN=$1
XP_DIR=$2
lambda=$3
batch_size=$4
save_every_k_batches=$5
num_models_to_save=$6
min_ram=$7
max_ram=$8
num_threads=$9
use_hierarchy=${10}
LOGS_DIR=${11}

if [ "${use_hierarchy}" = FALSE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0.jar"
fi

if [ "${use_hierarchy}" = TRUE ]; then
  CLASSPATH="$(dirname "${BASH_SOURCE[0]}")/../rofames-1.0.0-hier.jar"
fi

mkdir ${XP_DIR}/model 2> /dev/null

echo "Training ROFAMES parser..."

echo
echo "Argument Identification -- Step 1: Creating alphabet"
echo
${JAVA_HOME_BIN}/java \
    -classpath ${CLASSPATH} \
    -Xms${min_ram} \
    -Xmx${max_ram} \
    edu.cmu.cs.lti.ark.fn.parsing.CreateAlphabet \
    ${XP_DIR}/data/train.frame.elements \
    ${XP_DIR}/data/train.all.lemma.tags \
    ${XP_DIR}/model/train.events.bin \
    ${XP_DIR}/model/parser.conf \
    ${XP_DIR}/model/train.sentences.frame.elements.spans \
    true \
    1 \
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
