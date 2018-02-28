#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -x XP_NUM -t {mxpost,nlp4j} -p {rofames,open-sesame} [-d {mst,bmst,barch}] [-v]
Preprocess FrameNet train/dev/test splits.

  -h, --help                           display this help and exit
  -x, --xp      XP_NUM                 xp number written as 3 digits (e.g. 001)
  -t, --tagger  {mxpost,nlp4j}         pos tagger to be used: 'mxpost' or 'nlp4j'
  -p, --parser  {rofames,open-sesame}  frame semantic parser to be used: 'rofames' or 'open-sesame'
  -d, --dep     {mst,bmst,barch}       dependency parser to be used: 'mst', 'bmst' or 'barch'
  -v, --dev                            if set, script will also preprocess dev splits
EOF
}

is_xp_set=FALSE
is_tagger_set=FALSE
is_dep_parser_set=FALSE
is_fs_parser_set=FALSE
process_dev=FALSE
deparser=NONE

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
        -t|--tagger)
            if [ "$2" ]; then
                is_tagger_set=TRUE
                tagger=$2
                shift
            else
                die "ERROR: '--tagger' requires a non-empty option argument"
            fi
            ;;
        -d|--dep)
            if [ "$2" ]; then
                is_dep_parser_set=TRUE
                deparser=$2
                shift
            else
                die "ERROR: '--dep' requires a non-empty option argument"
            fi
            ;;
        -p|--parser)
            if [ "$2" ]; then
                is_fs_parser_set=TRUE
                fsparser=$2
                shift
            else
                die "ERROR: '--parser' requires a non-empty option argument"
            fi
            ;;
        -v|--dev)
            process_dev=TRUE
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

if [ "${is_tagger_set}" = FALSE ]; then
    die "ERROR: '--tagger' parameter is required."
fi

if [ "${is_fs_parser_set}" = FALSE ]; then
    die "ERROR: '--parser' parameter is required."
fi

case "${tagger}" in
    mxpost )
        ;;   #fallthru
    nlp4j )
        ;;   #fallthru
    * )
        die "Invalid pos tagger '${tagger}': Should be 'mxpost' or 'nlp4j'"
esac

case "${fsparser}" in
    rofames )
        ;;   #fallthru
    open-sesame )
        ;;   #fallthru
    * )
        die "Invalid frame semantic parser '${fsparser}': Should be 'rofames' or 'open-sesame'"
esac

if [ "${fsparser}" = "rofames" ]; then
  if [ "${is_dep_parser_set}" = FALSE ]; then
      die "ERROR: '--dep' parameter is required with --parser rofames."
  fi
  case "${deparser}" in
      mst )
          ;;   #fallthru
      bmst )
          ;;   #fallthru
      barch )
          ;;   #fallthru
      * )
          die "Invalid dependency parser '${deparser}': Should be 'mst', 'bmst' or 'barch'"
  esac
fi

echo "Initializing preprocessing..."
echo "Preprocessing setup:"
echo "  XP_DIR: ${XP_DIR}/${xp}"
echo "  POS tagger: ${tagger}"
echo "  Dependency parser: ${deparser}"
echo "  Frame semantic parser: ${fsparser}"

DATA_DIR=${XP_DIR}/${xp}/data

if [ "${tagger}" = "mxpost" ]; then
  bash ${SCRIPTS_DIR}/postag.sh -f ${DATA_DIR}/train.sentences -t mxpost
  bash ${SCRIPTS_DIR}/lemmatize.sh -f ${DATA_DIR}/train.sentences.conllx
  if [ "${process_dev}" = TRUE ]; then
    bash ${SCRIPTS_DIR}/postag.sh -f ${DATA_DIR}/dev.sentences -t mxpost
    bash ${SCRIPTS_DIR}/lemmatize.sh -f ${DATA_DIR}/dev.sentences.conllx
  fi
  bash ${SCRIPTS_DIR}/postag.sh -f ${DATA_DIR}/test.sentences -t mxpost
  bash ${SCRIPTS_DIR}/lemmatize.sh -f ${DATA_DIR}/test.sentences.conllx
fi

if [ "${tagger}" = "nlp4j" ]; then
  bash ${SCRIPTS_DIR}/postag.sh -f ${DATA_DIR}/train.sentences -t nlp4j
  if [ "${process_dev}" = TRUE ]; then
    bash ${SCRIPTS_DIR}/postag.sh -f ${DATA_DIR}/dev.sentences -t nlp4j
  fi
  bash ${SCRIPTS_DIR}/postag.sh -f ${DATA_DIR}/test.sentences -t nlp4j
fi

if [ "${deparser}" = "mst" ]; then
  bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/train.sentences.conllx -p mst
  if [ "${process_dev}" = TRUE ]; then
    bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/dev.sentences.conllx -p mst
  fi
  bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/test.sentences.conllx -p mst
fi

if [ "${deparser}" = "bmst" ]; then
  bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/train.sentences.conllx -p bmst
  if [ "${process_dev}" = TRUE ]; then
    bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/dev.sentences.conllx -p bmst
  fi
  bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/test.sentences.conllx -p bmst
fi

if [ "${deparser}" = "barch" ]; then
  bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/train.sentences.conllx -p barch
  if [ "${process_dev}" = TRUE ]; then
    bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/dev.sentences.conllx -p barch
  fi
  bash ${SCRIPTS_DIR}/deparse.sh -f ${DATA_DIR}/test.sentences.conllx -p barch
fi

if [ "${fsparser}" = "rofames" ]; then
  bash ${SCRIPTS_DIR}/flatten.sh -f ${DATA_DIR}/train.sentences.conllx
fi

if [ "${fsparser}" = "open-sesame" ]; then
  bash ${SCRIPTS_DIR}/merge.sh -b ${DATA_DIR}/dev.bios -c ${DATA_DIR}/dev.sentences.conllx
  bash ${SCRIPTS_DIR}/merge.sh -b ${DATA_DIR}/dev.bios.semeval -c ${DATA_DIR}/dev.sentences.conllx
  bash ${SCRIPTS_DIR}/merge.sh -b ${DATA_DIR}/test.bios -c ${DATA_DIR}/test.sentences.conllx
  bash ${SCRIPTS_DIR}/merge.sh -b ${DATA_DIR}/test.bios.semeval -c ${DATA_DIR}/test.sentences.conllx
  bash ${SCRIPTS_DIR}/merge.sh -b ${DATA_DIR}/train.bios -c ${DATA_DIR}/train.sentences.conllx
fi
