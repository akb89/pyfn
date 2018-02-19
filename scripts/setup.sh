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

export nlp4j_config="${RESOURCES_DIR}/config-decode-pos.xml"

die() {
    printf '%s\n' "$1" >&2
    exit 1
}
