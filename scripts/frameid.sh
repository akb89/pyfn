#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM
Perform frame identification.

  -h, --help                        display this help and exit
  -m, --mode                        train on all models or decode using a single model
  -x, --xp          XP_NUM          xp number written as 3 digits (e.g. 001)
EOF
}

is_xp_set=FALSE
is_mode_set=FALSE

while :; do
    case $1 in
        -h|-\?|--help)
            show_help
            exit
            ;;
        -x|--xp)
            if [ "$2" ]; then
                is_xp_set=TRUE
                xp="xp_$2"
                shift
            else
                die "ERROR: '--xp' requires a non-empty option argument"
            fi
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

if [ "${is_xp_set}" = FALSE ]; then
    die "ERROR: '--xp' parameter is required."
fi

if [ "${is_mode_set}" = FALSE ]; then
    die "ERROR: '--mode' parameter is required."
fi

echo "Preparing files for frame identification..."

mkdir ${XP_DIR}/${xp}/frameid 2> /dev/null
mkdir ${XP_DIR}/${xp}/frameid/data 2> /dev/null
mkdir ${XP_DIR}/${xp}/frameid/data/embeddings 2> /dev/null
mkdir ${XP_DIR}/${xp}/frameid/data/corpora 2> /dev/null
mkdir ${XP_DIR}/${xp}/frameid/data/lexicons 2> /dev/null

cp ${XP_DIR}/${xp}/data/test.frames ${XP_DIR}/${xp}/frameid/data/corpora/
cp ${XP_DIR}/${xp}/data/test.sentences.conllx ${XP_DIR}/${xp}/frameid/data/corpora/
cp ${XP_DIR}/${xp}/data/train.frame.elements ${XP_DIR}/${xp}/frameid/data/corpora/
cp ${XP_DIR}/${xp}/data/train.sentences.conllx.flattened ${XP_DIR}/${xp}/frameid/data/corpora/

cp ${RESOURCES_DIR}/deps.words.txt ${XP_DIR}/${xp}/frameid/data/embeddings/

mv ${XP_DIR}/${xp}/frameid/data/corpora/test.frames ${XP_DIR}/${xp}/frameid/data/corpora/test.frame.elements

bash ${SCRIPTS_DIR}/flatten.sh -f ${XP_DIR}/${xp}/frameid/data/corpora/test.sentences.conllx

python3 ${SIMFRAMEID_HOME}/generate.py ${XP_DIR}/${xp}/frameid/data/corpora/train.frame.elements ${XP_DIR}/${xp}/frameid/data/lexicons/fn_lexicon

echo "Done"

if [ "${mode}" = train ]; then
    echo "Training frame identification on all models..."
    python ${SIMFRAMEID_HOME}/simpleFrameId/main.py train ${XP_DIR}/${xp}/frameid
    echo "Done"
fi

if [ "${mode}" = decode ]; then
    echo "Predicting frames..."
    python ${SIMFRAMEID_HOME}/simpleFrameId/main.py decode ${XP_DIR}/${xp}/frameid
    echo "Done"
fi
