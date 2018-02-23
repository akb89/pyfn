#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XP_DIR -s {dev,test} -t {mxpost,nlp4j} [-u]
Train or decode with the ROFAMES parser.

  -h, --help                           display this help and exit
  -m, --mode          {train,decode}   rofames mode to use: train or decode
  -x, --xpdir         XP_DIR           absolute path to the xp directory (where data/ and model/ will be stored)
  -s, --splits        {dev,test}       which splits to use: dev or test
  -t, --tagger        {mxpost,nlp4j}   the POS tagger used for preprocessing splits
  -u, --use_hierarchy                  if specified, parser will use the hierarchy feature
EOF
}

is_mode_set=FALSE
is_xpdir_set=FALSE
use_hierarchy=FALSE
is_tagger_set=FALSE
is_splits_set=FALSE

while :; do
    case $1 in
        -h|-\?|--help)
            show_help
            exit
            ;;
        -m|--mode)
            if [ "$2" ]; then
                is_mode_set=TRUE
                mode=$2
                shift
            else
                die "ERROR: '--mode' requires a non-empty option argument"
            fi
            ;;
        -x|--xpdir)
            if [ "$2" ]; then
                is_xpdir_set=TRUE
                XPDIR=$2
                shift
            else
                die "ERROR: '--xpdir' requires a non-empty option argument"
            fi
            ;;
        -s|--splits)
            if [ "$2" ]; then
                is_splits_set=TRUE
                splits=$2
                shift
            else
                die "ERROR: '--splits' requires a non-empty option argument"
            fi
            ;;
        -t|--tagger)
            if [ "$2" ]; then
                is_tagger_set=TRUE
                tagger=$2
                shift
            else
                die "ERROR: '--tagger' requires a non-empty option argument"
            fi
            ;;
        -u|--use_hierarchy)
              use_hierarchy=TRUE
              shift
              ;;
        --)
            shift
            break
            ;;
        -?*)
            printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
            ;;
        *)
            break
    esac
    shift
done

if [ "${is_mode_set}" = FALSE ]; then
    die "ERROR: '--mode' parameter is required."
fi

if [ "${is_xpdir_set}" = FALSE ]; then
    die "ERROR: '--xpdir' parameter is required."
fi

if [ "${is_tagger_set}" = FALSE ]; then
    die "ERROR: '--tagger' parameter is required."
fi

if [ "${is_splits_set}" = FALSE ]; then
    die "ERROR: '--splits' parameter is required."
fi

case "${mode}" in
    train )
        ;;
    decode )
        ;;
    * )
        die "Invalid mode '${mode}': should be 'train' or 'decode'"
esac

case "${tagger}" in
    mxpost )
        ;;
    nlp4j )
        ;;
    * )
        die "Invalid POS tagger '${tagger}': should be 'mxpost' or 'nlp4j'"
esac

case "${splits}" in
    dev )
        ;;
    test )
        ;;
    * )
        die "Invalid splits '${splits}': should be 'dev' or 'test'"
esac

if [ "${mode}" = train ]; then
  bash ${ROFAMES_HOME}/bin/train.sh \
    ${JAVA_HOME_BIN} \
    ${XPDIR} \
    ${tagger}
    ${lambda} \
    ${kbest} \
    ${batch_size} \
    ${save_every_k_batches} \
    ${num_models_to_save} \
    ${min_ram} \
    ${max_ram} \
    ${num_threads} \
    ${use_hierarchy} \
    ${LOGS_DIR}
fi

if [ "${mode}" = decode ]; then
  bash ${ROFAMES_HOME}/bin/decode.sh \
    ${JAVA_HOME_BIN} \
    ${XPDIR} \
    ${splits} \
    ${tagger} \
    ${kbest} \
    ${max_ram} \
    ${use_hierarchy} \
    ${LOGS_DIR}
fi
