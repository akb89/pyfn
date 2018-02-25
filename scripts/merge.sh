#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -b BIOS_FILE -c CONLLX_FILE
Merge a .bios file with a .conllx file. Information from the .conllx file
is imported to the .bios file. Output file is in .bios format

  -h, --help                    display this help and exit
  -b, --bios      BIOS_FILE     absolute path to input .bios file
  -c, --conllx    CONLLX_FILE   absolute path to input .conllx file
EOF
}

is_input_bios_set=FALSE
is_input_conllx_set=FALSE

while :; do
    case $1 in
        -h|-\?|--help)
            show_help
            exit
            ;;
        -b|--bios)
            if [ "$2" ]; then
                is_input_bios_set=TRUE
                bios=$2
                shift
            else
                die "ERROR: '--bios' requires a non-empty option argument"
            fi
            ;;
        -c|--conllx)
            if [ "$2" ]; then
                is_input_conllx_set=TRUE
                conllx=$2
                shift
            else
                die "ERROR: '--conllx' requires a non-empty option argument"
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

if [ "${is_input_bios_set}" = FALSE ]; then
    die "ERROR: '--bios' parameter is required."
fi

if [ "${is_input_conllx_set}" = FALSE ]; then
    die "ERROR: '--conllx' parameter is required."
fi

crb_split() {
    local STOP=$1
    local IN=$2
    local OUT=$3
    local DIR=$4
    perl -pe "s/^$/$STOP/g" $IN > $OUT
    cd $DIR
    csplit -s -k -f "" -n 10 $OUT "/_ù_ù_/" "{2000000}" 2> /dev/null
    cd -
}

merge_bios_conllx() {
  local INPUT_BIOS_FILE=$1
  local INPUT_CONLLX_FILE=$2
  local OUTPUT_FILE=${INPUT_BIOS_FILE}.merged
  local OUTPUT_TMP_FILE="/tmp/file.txt"
  local OUTPUT_TMP_DIR="/tmp/outdir"
  local OUTPUT_TMP_BIOS_DIR="/tmp/splitted_bios"
  local OUTPUT_TMP_CONLLX_DIR="/tmp/splitted_conllx"

  rm ${OUTPUT_TMP_FILE} 2> /dev/null
  rm -rf ${OUTPUT_TMP_DIR} 2> /dev/null
  rm -rf ${OUTPUT_TMP_BIOS_DIR} 2> /dev/null
  rm -rf ${OUTPUT_TMP_CONLLX_DIR} 2> /dev/null
  mkdir ${OUTPUT_TMP_BIOS_DIR} 2> /dev/null
  mkdir ${OUTPUT_TMP_CONLLX_DIR} 2> /dev/null
  mkdir ${OUTPUT_TMP_DIR} 2> /dev/null

  RM_STOP="_ù_ù_"

  crb_split ${RM_STOP} ${INPUT_BIOS_FILE} ${OUTPUT_TMP_FILE} ${OUTPUT_TMP_BIOS_DIR}
  crb_split ${RM_STOP} ${INPUT_CONLLX_FILE} ${OUTPUT_TMP_FILE} ${OUTPUT_TMP_CONLLX_DIR}


  for i in $(find ${OUTPUT_TMP_BIOS_DIR} -iname "0*" -print0 | sort -z | xargs -0 | tr " " "\n"); do
      LN=$(grep -v $RM_STOP $i | wc -l | perl -pe "s/\s+//g")
      if [[ $LN -eq 0 ]]; then
          continue;
      fi;
      SENT_IDX=$(grep -v ${RM_STOP} ${i} | cut -f 7 | head -1)
      PADDED_INT=$(printf "%010d" ${SENT_IDX})

      BIOS_FILE=${OUTPUT_TMP_DIR}/tmp.bios
      CONLLX_FILE=${OUTPUT_TMP_DIR}/tmp.conllx

      grep -v ${RM_STOP} ${OUTPUT_TMP_CONLLX_DIR}/${PADDED_INT}  > ${CONLLX_FILE}
      grep -v ${RM_STOP} $i > ${BIOS_FILE}

      cut -f 1-3 ${BIOS_FILE} > ${OUTPUT_TMP_DIR}/id.form.lemma
      cut -f 3 ${CONLLX_FILE} > ${OUTPUT_TMP_DIR}/plemma
      cut -f 5 ${BIOS_FILE} > ${OUTPUT_TMP_DIR}/pos
      cut -f 4 ${CONLLX_FILE} > ${OUTPUT_TMP_DIR}/ppos
      cut -f 7-9 ${BIOS_FILE} > ${OUTPUT_TMP_DIR}/feat.pfeat.head
      cut -f 7 ${CONLLX_FILE} > ${OUTPUT_TMP_DIR}/phead
      cut -f 11 ${BIOS_FILE} > ${OUTPUT_TMP_DIR}/deprel
      cut -f 8 ${CONLLX_FILE} > ${OUTPUT_TMP_DIR}/pdeprel
      cut -f 13-16 ${BIOS_FILE} > ${OUTPUT_TMP_DIR}/lu.frame.fe.fecoretype

      paste ${OUTPUT_TMP_DIR}/id.form.lemma ${OUTPUT_TMP_DIR}/plemma ${OUTPUT_TMP_DIR}/pos ${OUTPUT_TMP_DIR}/ppos ${OUTPUT_TMP_DIR}/feat.pfeat.head ${OUTPUT_TMP_DIR}/phead ${OUTPUT_TMP_DIR}/deprel ${OUTPUT_TMP_DIR}/pdeprel ${OUTPUT_TMP_DIR}/lu.frame.fe.fecoretype | perl -pe "s/^\t+$//g" | cat -s >> ${OUTPUT_FILE}
      echo "" >> ${OUTPUT_FILE}
  done

  rm -rf ${OUTPUT_TMP_BIOS_DIR}
  rm -rf ${OUTPUT_TMP_CONLLX_DIR}
  rm -rf ${OUTPUT_TMP_DIR}
}

echo "Merging .conllx content to .bios file for the open-sesame parser..."
echo "Processing .bios file: ${bios}"
echo "Processing .conllx file: ${conllx}"
merge_bios_conllx $bios $conllx
