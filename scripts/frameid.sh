#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -x XP_NUM [-a]
Perform frame identification.

  -h, --help                        display this help and exit
  -x, --xp          XP_NUM          xp number written as 3 digits (e.g. 001)
  -a, --all                         perform frame identification using all models
EOF
}

is_xp_set=FALSE
use_all_models=FALSE

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
        -a|--all)
            use_all_models=TRUE
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

if [ "${use_all_models}" = TRUE ]; then
    echo "Starting frame identification on all models..."
    python ${SIMFRAMEID_HOME}/simpleFrameId/main.py ${XP_DIR}/${xp}/frameid
    echo "Done"
fi

if [ "${use_all_models}" = FALSE ]; then
    echo "Starting frame identification on all models..."

    echo "Done"
fi
