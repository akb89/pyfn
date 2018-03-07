#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-s {dev,test}] [-d] [-u]
Train or decode with the OPEN-SESAME parser.

  -h, --help                              display this help and exit
  -m, --mode              {train,decode}  open-sesame mode to use: train or decode
  -x, --xp                XP_NUM          xp number written as 3 digits (e.g. 001)
  -s, --splits            {dev,test}      which splits to use in decode mode: dev or test
  -d, --with_dep_parses                   if specified, parser will use dependency parses
  -u, --with_hierarchy                    if specified, parser will use the hierarchy feature
EOF
}

is_mode_set=FALSE
is_xp_set=FALSE
is_splits_set=FALSE
with_dep_parses=FALSE

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
        -d|--with_dep_parses)
            with_dep_parses=TRUE
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
    die "ERROR: '--mode' parameter is required"
fi

if [ "${is_xp_set}" = FALSE ]; then
    die "ERROR: '--xp' parameter is required"
fi

case "${mode}" in
    train )
        ;;
    decode )
        ;;
    * )
        die "Invalid mode '${mode}': should be 'train' or 'decode'"
esac

if [ "${mode}" = decode ]; then
  if [ "${is_splits_set}" = FALSE ]; then
      die "ERROR: '--splits' parameter is required for decoding"
  fi
  case "${splits}" in
      dev )
          ;;
      test )
          ;;
      * )
          die "Invalid splits '${splits}': should be 'dev' or 'test'"
  esac
fi

mkdir ${XP_DIR}/${xp}/model 2> /dev/null

postprocess_decoded_file() {
  BIOS_FILE=$1
  DECODED_FILE=$2
  OUTPUT_TMP_DIR="/tmp/biospost"

  rm -rf $OUTPUT_TMP_DIR 2> /dev/null
  mkdir $OUTPUT_TMP_DIR 2> /dev/null

  cut -f 1-14 ${BIOS_FILE} > ${OUTPUT_TMP_DIR}/cutted.1.txt
  cut -f 15 ${DECODED_FILE} > ${OUTPUT_TMP_DIR}/cutted.2.txt

  paste ${OUTPUT_TMP_DIR}/cutted.1.txt ${OUTPUT_TMP_DIR}/cutted.2.txt  | perl -pe "s/^\t+$//g" | cat -s > ${DECODED_FILE}

  rm -rf $OUTPUT_TMP_DIR;
}

if [ "${mode}" = train ]; then
  if [ "${with_dep_parses}" = TRUE ]; then
    python ${OPEN_SESAME_HOME}/src/segrnn-argid.py \
      --model ${XP_DIR}/${xp}/model/segrnn.argid.model \
      --trainf ${XP_DIR}/${xp}/data/train.bios \
      --devf ${XP_DIR}/${xp}/data/dev.bios \
      --vecf ${XP_DIR}/${xp}/data/glove.6B.100d.txt \
      --syn dep
  fi
  if [ "${with_dep_parses}" = FALSE ]; then
    python ${OPEN_SESAME_HOME}/src/segrnn-argid.py \
      --model ${XP_DIR}/${xp}/model/segrnn.argid.model \
      --trainf ${XP_DIR}/${xp}/data/train.bios \
      --devf ${XP_DIR}/${xp}/data/dev.bios \
      --vecf ${XP_DIR}/${xp}/data/glove.6B.100d.txt
  fi
fi

if [ "${mode}" = decode ]; then
  if [ "${with_dep_parses}" = TRUE ]; then
    python ${OPEN_SESAME_HOME}/src/segrnn-argid.py \
      --mode test \
      --model ${XP_DIR}/${xp}/model/segrnn.argid.model \
      --trainf ${XP_DIR}/${xp}/data/train.bios \
      --testf ${XP_DIR}/${xp}/data/${splits}.bios.semeval \
      --vecf ${XP_DIR}/${xp}/data/glove.6B.100d.txt \
      --syn dep
  fi
  if [ "${with_dep_parses}" = FALSE ]; then
    python ${OPEN_SESAME_HOME}/src/segrnn-argid.py \
      --mode test \
      --model ${XP_DIR}/${xp}/model/segrnn.argid.model \
      --trainf ${XP_DIR}/${xp}/data/train.bios \
      --testf ${XP_DIR}/${xp}/data/${splits}.bios.semeval \
      --vecf ${XP_DIR}/${xp}/data/glove.6B.100d.txt
  fi
    postprocess_decoded_file ${XP_DIR}/${xp}/data/${splits}.bios.semeval ${XP_DIR}/${xp}/data/${splits}.bios.semeval.decoded
fi
