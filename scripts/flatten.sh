#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE
Flatten .conllx file to ROFAMES .all.lemma.tags file.

  -h, --help          display this help and exit
  -f, --file   FILE   absolute path to input .conllx file
EOF
}

is_input_file_set=FALSE

while :; do
    case $1 in
        -h|-\?|--help)
            show_help
            exit
            ;;
        -f|--file)
            if [ "$2" ]; then
                is_input_file_set=TRUE
                file=$2
                shift
            else
                die "ERROR: '--file' requires a non-empty option argument"
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

if [ "${is_input_file_set}" = FALSE ]; then
    die "ERROR: '--file' parameter is required."
fi

flatten_conllx_to_all_lemma_tags() {
  INPUT_FILE=$1
  OUTPUT_FINAL_FILE=$2
  OUTPUT_TMP_FILE="/tmp/file.txt"
  OUTPUT_TMP_DIR="/tmp/splitted"

  rm $OUTPUT_TMP_FILE 2> /dev/null
  rm $OUTPUT_FINAL_FILE 2> /dev/null
  mkdir $OUTPUT_TMP_DIR 2> /dev/null

  perl -pe "s/^$/_ù_ù_/g" $INPUT_FILE > $OUTPUT_TMP_FILE

  cd $OUTPUT_TMP_DIR;

  csplit -s -k -f "" -n 10 $OUTPUT_TMP_FILE "/_ù_ù_/" "{2000000}" 2> /dev/null

  RM_STOP="_ù_ù_"

  for i in $(find -s $OUTPUT_TMP_DIR -iname "0*"); do
      LN=$(grep -v $RM_STOP $i | wc -l | perl -pe "s/\s+//g")
      if [[ $LN -eq 0 ]]; then
          continue;
      fi;

      TOKENS=$(grep -v $RM_STOP $i | cut -f 2 | tr "\n" "\t")
      POS=$(grep -v $RM_STOP $i | cut -f 4 | tr "\n" "\t")
      LABELS_DEP=$(grep -v $RM_STOP $i | cut -f 8 | tr "\n" "\t")
      INDEXES_DEP=$(grep -v $RM_STOP $i | cut -f 7 | tr "\n" "\t")
      OO=$(grep -v $RM_STOP $i  | cut -f 1 | perl -pe "s/[0-9]+/O/g" | tr "\n" "\t")
      LEMMAS=$(grep -v $RM_STOP $i | cut -f 3 | tr "\n" "\t")

      echo -e "${LN}\t${TOKENS}${POS}${LABELS_DEP}${INDEXES_DEP}${OO}${LEMMAS}" >> $OUTPUT_FINAL_FILE
  done;

  rm -rf $OUTPUT_TMP_DIR;
  cd -
}

flatten_conllx_to_all_lemma_tags $file $file.flattened
