#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -x XP_NUM -p {semafor,open-sesame} -s {dev,test} -f FN_DATA_DIR [-u] [-e]
Preprocess FrameNet train/dev/test splits.

  -h, --help                                   display this help and exit
  -x, --xp              XP_NUM                 xp number written as 3 digits (e.g. 001)
  -p, --parser          {semafor,open-sesame}  frame semantic parser to be used: 'semafor' or 'open-sesame'
  -s, --splits          {dev,test}             which splits to score: dev or test
  -u, --with_hierarchy                         if specified, will use the hierarchy feature
  -e, --with_exemplars                         if specified, will use the exemplars
  -f, --fn              FN_DATA_DIR            absolute path to FrameNet data directory
EOF
}

is_xp_set=FALSE
is_parser_set=FALSE
is_splits_set=FALSE
is_fndir_set=FALSE
with_hierarchy=FALSE
with_exemplars=FALSE

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
        -p|--parser)
            if [ "$2" ]; then
                is_parser_set=TRUE
                parser=$2
                shift
            else
                die "ERROR: '--parser' requires a non-empty option argument"
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
        -f|--fn)
            if [ "$2" ]; then
                is_fndir_set=TRUE
                FN_DATA_DIR=$2
                shift
            else
                die "ERROR: '--fn' requires a non-empty option argument"
            fi
            ;;
        -u|--with_hierarchy)
              with_hierarchy=TRUE
              shift
              ;;
        -e|--with_exemplars)
              with_exemplars=TRUE
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

if [ "${is_xp_set}" = FALSE ]; then
    die "ERROR: '--xp' parameter is required."
fi

if [ "${is_parser_set}" = FALSE ]; then
    die "ERROR: '--parser' parameter is required."
fi

if [ "${is_splits_set}" = FALSE ]; then
    die "ERROR: '--splits' parameter is required."
fi

if [ "${is_fndir_set}" = FALSE ]; then
    die "ERROR: '--fn' parameter is required."
fi

case "${splits}" in
    dev )
        ;;
    test )
        ;;
    * )
        die "Invalid splits '${splits}': should be 'dev' or 'test'"
esac

case "${parser}" in
    semafor )
        ;;   #fallthru
    open-sesame )
        ;;   #fallthru
    * )
        die "Invalid frame semantic parser '${parser}': Should be 'semafor' or 'open-sesame'"
esac

echo "Generating gold SEMEVAL XML file..."
pyfn convert \
  --from fnxml \
  --to semeval \
  --source "${FN_DATA_DIR}" \
  --target "${XP_DIR}/${xp}/data" \
  --splits "${splits}"
echo "Done"

if [ "${parser}" = "semafor" ]; then
  echo "Creating framenet.frame.element.map from train splits..."
  ${JAVA_HOME_BIN}/java \
      -classpath "${SEMAFOR_HOME}/rofames-1.0.0.jar" \
      -Xmx${max_ram} \
      edu.unige.clcl.fn.data.prep.training.maps.FEMap \
      "${XP_DIR}/${xp}/data/train.frame.elements" \
      "${XP_DIR}/${xp}/data/framenet.frame.element.map"
  echo "Done creating framenet.original.map and framenet.frame.element.map"
  echo "Copying frames.xml file to XP data directory"
  cp ${FN_DATA_DIR}/frames.xml ${XP_DIR}/${xp}/data
  echo "Copying frRelations.xml file to XP data directory"
  cp ${FN_DATA_DIR}/frRelations.xml ${XP_DIR}/${xp}/data
  if [ "${with_hierarchy}" = TRUE ]; then
    echo "Generating hierarchy .csv files..."
    if [ "${with_exemplars}" = TRUE ]; then
      echo "using exemplars..."
      pyfn generate \
        --source "${FN_DATA_DIR}" \
        --target "${XP_DIR}/${xp}/data" \
        --with_exemplars
    fi
    if [ "${with_exemplars}" = FALSE ]; then
      echo "without exemplars..."
      pyfn generate \
        --source "${FN_DATA_DIR}" \
        --target "${XP_DIR}/${xp}/data"
    fi
    echo "Done"
  fi
fi

if [ "${parser}" = "open-sesame" ]; then
  echo "Copying glove.6B.100d.txt file to XP data directory"
  cp ${FN_DATA_DIR}/glove.6B.100d.txt ${XP_DIR}/${xp}/data
  echo "Copying frames.xml file to XP data directory"
  cp ${FN_DATA_DIR}/frames.xml ${XP_DIR}/${xp}/data
  echo "Copying frRelations.xml file to XP data directory"
  cp ${FN_DATA_DIR}/frRelations.xml ${XP_DIR}/${xp}/data
fi
