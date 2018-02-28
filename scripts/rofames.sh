#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-s {dev,test}] [-u]
Train or decode with the ROFAMES parser.

  -h, --help                             display this help and exit
  -m, --mode            {train,decode}   rofames mode to use: train or decode
  -x, --xp              XP_NUM           xp number written as 3 digits (e.g. 001)
  -s, --splits          {dev,test}       which splits to use in decode mode: dev or test
  -u, --with_hierarchy                   if specified, parser will use the hierarchy feature
EOF
}

is_mode_set=FALSE
is_xp_set=FALSE
is_splits_set=FALSE
with_hierarchy=FALSE

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
        -x|--xp)
            if [ "$2" ]; then
                is_xp_set=TRUE
                xp="xp_$2"
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
        -u|--with_hierarchy)
              with_hierarchy=TRUE
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

if [ "${is_xp_set}" = FALSE ]; then
    die "ERROR: '--xp' parameter is required."
fi

case "${mode}" in
    train )
        ;;
    decode )
        ;;
    * )
        die "Invalid mode '${mode}': should be 'train' or 'decode'"
esac

mkdir ${LOGS_DIR} 2> /dev/null

if [ "${mode}" = train ]; then
  bash ${ROFAMES_HOME}/bin/train.sh \
    ${JAVA_HOME_BIN} \
    ${XP_DIR}/${xp} \
    ${lambda} \
    ${kbest} \
    ${batch_size} \
    ${save_every_k_batches} \
    ${num_models_to_save} \
    ${min_ram} \
    ${max_ram} \
    ${num_threads} \
    ${with_hierarchy} \
    ${LOGS_DIR}
fi

if [ "${mode}" = decode ]; then
  if [ "${is_splits_set}" = FALSE ]; then
      die "ERROR: '--splits' parameter is required."
  fi
  case "${splits}" in
      dev )
          ;;
      test )
          ;;
      * )
          die "Invalid splits '${splits}': should be 'dev' or 'test'"
  esac
  bash ${ROFAMES_HOME}/bin/decode.sh \
    ${JAVA_HOME_BIN} \
    ${XP_DIR}/${xp} \
    ${splits} \
    ${kbest} \
    ${max_ram} \
    ${with_hierarchy} \
    ${LOGS_DIR}
fi
