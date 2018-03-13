#!/bin/bash

# SEMAFOR options to be changed according to your env
export JAVA_HOME_BIN="/Library/Java/JavaVirtualMachines/jdk1.8.0_20.jdk/Contents/Home/bin"
export num_threads=2
export min_ram=4g # min RAM allocated to the JVM in GB. Corresponds to the -Xms argument
export max_ram=8g # max RAM allocated to the JVM in GB. Corresponds to the -Xmx argument

# SEMAFOR/SEMAFOR hyperparameters
export kbest=1 # keep k-best parse
export lambda=0.000001 # hyperparameter for argument identification. Refer to Kshirsagar et al. (2015) for details.
export batch_size=4000 # number of batches processed at once for argument identification.
export save_every_k_batches=400 # for argument identification
export num_models_to_save=60 # for argument identification

# Do not change the following
export SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export XP_DIR="${SCRIPTS_DIR}/../experiments"
export RESOURCES_DIR="${SCRIPTS_DIR}/../resources"
export LIB_DIR="${SCRIPTS_DIR}/../lib"
export LOGS_DIR="${SCRIPTS_DIR}/../log"

export MXPOST_HOME="${LIB_DIR}/jmx"
export NLP4J_HOME="${LIB_DIR}/nlp4j"
export MST_PARSER_HOME="${LIB_DIR}/mstparser"
export BMST_PARSER_HOME="${LIB_DIR}/bistparser/bmstparser/src"
export BARCH_PARSER_HOME="${LIB_DIR}/bistparser/barchybrid/src"
export SEMAFOR_HOME="${LIB_DIR}/semafor"
export OPEN_SESAME_HOME="${LIB_DIR}/open-sesame"
export SEMEVAL_HOME="${LIB_DIR}/semeval"
export SIMFRAMEID_HOME="${LIB_DIR}/eacl2017-oodFrameNetSRL"

export nlp4j_config="${RESOURCES_DIR}/config-decode-pos.xml"
export mst_parser_model="${RESOURCES_DIR}/wsj.model"
export bist_external_vectors="${RESOURCES_DIR}/sskip.100.vectors"
export barch_model="${RESOURCES_DIR}/bestarchybrid.model"
export barch_params="${RESOURCES_DIR}/bestarchybrid.params"
export bmst_model="${RESOURCES_DIR}/bestfirstorder.model"
export bmst_params="${RESOURCES_DIR}/bestfirstorder.params"

die() {
    printf '%s\n' "$1" >&2
    exit 1
}
