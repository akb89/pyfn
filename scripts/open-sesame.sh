#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-s {dev,test}] [-d] [-u]
Train or decode with the OPEN-SESAME parser.

  -h, --help                          display this help and exit
  -m, --mode          {train,decode}  open-sesame mode to use: train or decode
  -x, --xp            XP_NUM          xp number written as 3 digits (e.g. 001)
  -s, --splits        {dev,test}      which splits to use in decode mode: dev or test
  -d, --dep                           if specified, parser will use dependency parses
  -u, --use_hierarchy                 if specified, parser will use the hierarchy feature
EOF
}

is_mode_set=FALSE
is_xp_set=FALSE

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

mkdir ${XP_DIR}/${xp}/model 2> /dev/null

if [ "${mode}" = train ]; then
  python ${OPEN_SESAME_HOME}/src/segrnn-argid.py \
    --model ${XP_DIR}/${xp}/model/segrnn.argid.model \
    --trainf ${XP_DIR}/${xp}/data/train.bios.merged \
    --devf ${XP_DIR}/${xp}/data/dev.bios.merged \
    --vecf ${XP_DIR}/${xp}/data/glove.6B.100d.framevocab.txt
fi
