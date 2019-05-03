#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XP_NUM [-p {semafor,open-sesame}]
Perform frame identification.

  -h, --help                            display this help and exit
  -m, --mode                            train on all models or decode using a single model
  -x, --xp       XP_NUM                 xp number written as 3 digits (e.g. 001)
  -p, --parser   {semafor,open-sesame}  formalize decoded frames for specified parser
  -e, --embed                           name of embeddings to use
EOF
}

is_xp_set=FALSE
is_mode_set=FALSE
is_parser_set=FALSE
is_embed_set=FALSE

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
        -p|--parser)
            if [ "$2" ]; then
                is_parser_set=TRUE
                parser=$2
                shift
            else
                die "ERROR: '--parser' requires a non-empty option argument"
            fi
            ;;
        -e|--embed)
            if [ "$2" ]; then
                is_embed_set=TRUE
                embed=$2
                shift
            else
                die "ERROR: '--embed' requires a non-empty option argument"
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

prepare() {
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

  cp ${RESOURCES_DIR}/${embed} ${XP_DIR}/${xp}/frameid/data/embeddings/

  mv ${XP_DIR}/${xp}/frameid/data/corpora/test.frames ${XP_DIR}/${xp}/frameid/data/corpora/test.frame.elements

  bash ${SCRIPTS_DIR}/flatten.sh -f ${XP_DIR}/${xp}/frameid/data/corpora/test.sentences.conllx

  python3 ${SIMFRAMEID_HOME}/generate.py ${XP_DIR}/${xp}/frameid/data/corpora/train.frame.elements ${XP_DIR}/${xp}/frameid/data/lexicons/fn_lexicon

  echo "Done"
}

if [ "${mode}" = train ]; then
  prepare
  echo "Training frame identification on all models..."
  python ${SIMFRAMEID_HOME}/simpleFrameId/main.py train ${XP_DIR}/${xp}/frameid ${embed}
  echo "Done"
fi

if [ "${mode}" = decode ]; then
  if [ "${is_parser_set}" = FALSE ]; then
      die "ERROR: '--parser' parameter is required."
  fi
  case "${parser}" in
      semafor )
          ;;   #fallthru
      open-sesame )
          ;;   #fallthru
      * )
          die "Invalid frame semantic parser '${parser}': Should be 'semafor' or 'open-sesame'"
  esac
  prepare
  echo "Predicting frames..."
  python ${SIMFRAMEID_HOME}/simpleFrameId/main.py decode ${XP_DIR}/${xp}/frameid ${embed}
  echo "Done"
  if [ "${parser}" = semafor ]; then
    cut -f 1-3 ${XP_DIR}/${xp}/data/test.frames > ${XP_DIR}/${xp}/data/test.frames.cut.1.txt
    cut -f 5-8 ${XP_DIR}/${xp}/data/test.frames > ${XP_DIR}/${xp}/data/test.frames.cut.2.txt
    paste ${XP_DIR}/${xp}/data/test.frames.cut.1.txt ${XP_DIR}/${xp}/frameid/test.frames.predicted ${XP_DIR}/${xp}/data/test.frames.cut.2.txt | perl -pe "s/^\t+$//g" | cat -s > ${XP_DIR}/${xp}/data/test.frames
    rm ${XP_DIR}/${xp}/data/test.frames.cut.1.txt
    rm ${XP_DIR}/${xp}/data/test.frames.cut.2.txt
  fi
  if [ "${parser}" = open-sesame ]; then
    python3 CoNLLizer.py merger -c ${XP_DIR}/${xp}/data/test.bios.semeval -P ${XP_DIR}/${xp}/frameid/test.frames.predicted -n 14 -N 1 > ${XP_DIR}/${xp}/data/test.bios.semeval.merged
    mv ${XP_DIR}/${xp}/data/test.bios.semeval.merged ${XP_DIR}/${xp}/data/test.bios.semeval
  fi
fi
