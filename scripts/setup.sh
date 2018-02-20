#!/bin/bash

# Change the following settings according to your environment
export num_threads=2

# Do not change the followings
export SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export RESOURCES_DIR="${SCRIPTS_DIR}/../resources"
export LIB_DIR="${SCRIPTS_DIR}/../lib"
export LOGS_DIR="${SCRIPTS_DIR}/../log"

export MXPOST_HOME="${LIB_DIR}/jmx"
export NLP4J_HOME="${LIB_DIR}/nlp4j"
export BMST_PARSER_HOME="${LIB_DIR}/bistparser/bmstparser/src"

export nlp4j_config="${RESOURCES_DIR}/config-decode-pos.xml"
export bist_external_vectors="${RESOURCES_DIR}/sskip.100.vectors"
export barch_model="${RESOURCES_DIR}/bestarchybrid.model"
export barch_params="${RESOURCES_DIR}/bestarchybrid.params"
export bmst_model="${RESOURCES_DIR}/bestfirstorder.model"
export bmst_params="${RESOURCES_DIR}/bestfirstorder.params"

die() {
    printf '%s\n' "$1" >&2
    exit 1
}
