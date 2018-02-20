#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

# Usage info
show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE -t {mxpost,nlp4j}
Part-of-speech tag a given .sentences file with a specified tagger.

  -h, --help           display this help and exit
  -f, --file   FILE    absolute path to input .sentences file
  -t, --tagger TAGGER  POS tagger to be used: 'mxpost' or 'nlp4j'
EOF
}

convert_mxpost_to_conllx() {
  INPUT_FILE=$1
  OUTPUT_FINAL_FILE=$2
  OUTPUT_TMP_FILE="/tmp/file.txt"
  OUTPUT_TMP_DIR="/tmp/splitted"

  rm $OUTPUT_TMP_FILE 2> /dev/null
  rm $OUTPUT_FINAL_FILE 2> /dev/null
  mkdir $OUTPUT_TMP_DIR; 2> /dev/null

  perl -pe "s/ +/\n/g" $INPUT_FILE | perl -pe "s/_/\t/g" | perl -pe "s/^$/_ù_ù_/g" > $OUTPUT_TMP_FILE

  cd $OUTPUT_TMP_DIR;
  csplit -s -k -f "" -n 10 $OUTPUT_TMP_FILE "/_ù_ù_/" "{2000000}" 2> /dev/null

  for i in $(ls $OUTPUT_TMP_DIR/*); do
      perl -pe "s/_ù_ù_//g" $i | grep -v "^$" | nl -w3 | perl -pe "s/^ +//g" >> $OUTPUT_FINAL_FILE
      echo "" >> $OUTPUT_FINAL_FILE
  done;

  cut -f 1 $OUTPUT_FINAL_FILE > $OUTPUT_TMP_DIR/cutted.1.txt
  cut -f 2 $OUTPUT_FINAL_FILE > $OUTPUT_TMP_DIR/cutted.2.txt
  cut -f 3 $OUTPUT_FINAL_FILE > $OUTPUT_TMP_DIR/cutted.3.txt
  perl -pe "s/[0-9]+/_/g" $OUTPUT_TMP_DIR/cutted.1.txt > $OUTPUT_TMP_DIR/cutted.0.txt

  paste $OUTPUT_TMP_DIR/cutted.1.txt $OUTPUT_TMP_DIR/cutted.2.txt $OUTPUT_TMP_DIR/cutted.0.txt $OUTPUT_TMP_DIR/cutted.3.txt $OUTPUT_TMP_DIR/cutted.3.txt $OUTPUT_TMP_DIR/cutted.0.txt $OUTPUT_TMP_DIR/cutted.0.txt $OUTPUT_TMP_DIR/cutted.0.txt $OUTPUT_TMP_DIR/cutted.0.txt $OUTPUT_TMP_DIR/cutted.0.txt | perl -pe "s/^\t+$//g" | sed -e '$ d' > $OUTPUT_FINAL_FILE

  rm -rf $OUTPUT_TMP_DIR;

}

convert_sentences_to_tsv() {
  INPUT_FILE=$1
  OUTPUT_FINAL_FILE=$2
  OUTPUT_TMP_FILE="/tmp/file.txt"
  OUTPUT_TMP_DIR="/tmp/splitted"

  rm ${OUTPUT_TMP_FILE} 2> /dev/null
  rm ${OUTPUT_FINAL_FILE} 2> /dev/null
  mkdir ${OUTPUT_TMP_DIR};

  perl -pe "s/\n/\ _ù_ù_\n/g" ${INPUT_FILE} | perl -pe "s/\s+/\n/g" | perl -i -n -e 'print if /\S/' | perl -pe "s/\_ù_ù_//g" > ${OUTPUT_TMP_FILE}
  #perl -i -n -e 'print if /\S/' ${OUTPUT_TMP_FILE}
  #perl -pe "s/\_ù_ù_//g" ${OUTPUT_TMP_FILE} > ${OUTPUT_TMP_FILE}

  cd ${OUTPUT_TMP_DIR};
  csplit -s -k -f "" -n 10 ${OUTPUT_TMP_FILE} "/_ù_ù_/" "{2000000}" 2> /dev/null
  #
  # for i in $(ls ${OUTPUT_TMP_DIR}/*); do
  #     perl -pe "s/_ù_ù_//g" $i | grep -v "^$" | nl -w3 | perl -pe "s/^ +//g" >> ${OUTPUT_FINAL_FILE}
  #     echo "" >> ${OUTPUT_FINAL_FILE}
  # done;
  #
  # cut -f 1 ${OUTPUT_FINAL_FILE} > ${OUTPUT_TMP_DIR}/cutted.1.txt
  # cut -f 2 ${OUTPUT_FINAL_FILE} > ${OUTPUT_TMP_DIR}/cutted.2.txt
  # cut -f 3 ${OUTPUT_FINAL_FILE} > ${OUTPUT_TMP_DIR}/cutted.3.txt
  # perl -pe "s/[0-9]+/_/g" ${OUTPUT_TMP_DIR}/cutted.1.txt > ${OUTPUT_TMP_DIR}/cutted.0.txt
  #
  # paste ${OUTPUT_TMP_DIR}/cutted.1.txt ${OUTPUT_TMP_DIR}/cutted.2.txt ${OUTPUT_TMP_DIR}/cutted.0.txt ${OUTPUT_TMP_DIR}/cutted.3.txt ${OUTPUT_TMP_DIR}/cutted.0.txt ${OUTPUT_TMP_DIR}/cutted.0.txt ${OUTPUT_TMP_DIR}/cutted.0.txt ${OUTPUT_TMP_DIR}/cutted.0.txt ${OUTPUT_TMP_DIR}/cutted.0.txt ${OUTPUT_TMP_DIR}/cutted.0.txt | perl -pe "s/^\t+$//g" | sed -e '$ d' > ${OUTPUT_FINAL_FILE}
  #
  # rm -rf ${OUTPUT_TMP_DIR};
}

is_input_file_set=FALSE
is_tagger_set=FALSE

while :; do
    case $1 in
        -h|-\?|--help)
            show_help
            exit
            ;;
        -f|--file)       # Takes an option argument; ensure it has been specified.
            if [ "$2" ]; then
                is_input_file_set=TRUE
                file=$2
                shift
            else
                die "ERROR: '--file' requires a non-empty option argument"
            fi
            ;;
        -t|--tagger)       # Takes an option argument; ensure it has been specified.
            if [ "$2" ]; then
                is_tagger_set=TRUE
                tagger=$2
                shift
            else
                die "ERROR: '--tagger' requires a non-empty option argument"
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

if [ "${is_tagger_set}" = FALSE ]; then
    die "ERROR: '--tagger' parameter is required."
fi

case "${tagger}" in
    mxpost )
        ;;   #fallthru
    nlp4j )
        ;;   #fallthru
    * )
        die "Invalid POS tagger '${tagger}': Should be 'mxpost' or 'nlp4j'"
esac

echo "Initializing part-of-speech tagging..."

if [ "${tagger}" = "mxpost" ]; then
    echo "POS tagging via MXPOST..."
    pushd ${MXPOST_HOME}
    ./mxpost tagger.project < ${file} > ${file}.mxpost 2> ${LOGS_DIR}/mxpost.log
    echo "Done"
    echo "Converting .mxpost file to .conllx format..."
    convert_mxpost_to_conllx ${file}.mxpost ${file}.mxpost.conllx
    echo "Done"
fi

if [ "${tagger}" = "nlp4j" ]; then
    echo "Converting .sentences to .tsv format..."
    convert_sentences_to_tsv ${file} ${file}.tsv
    echo "Done"
    echo "POS tagging via NLP4J..."
    sh ${NLP4J_HOME}/bin/nlpdecode \
      -c ${nlp4j_config} \
      -format tsv \
      -i ${file}.tsv \
      -oe nlp4j \
      -threads ${num_threads} > ${LOGS_DIR}/nlp4j.log
    echo "Done"
    echo "Converting .nlp4j to .conllx format..."
    #convert_nlp4j_to_conllx ${file}.tsv.nlp4j ${file}.nlp4j.conllx
    echo "Done"
fi
