#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

# Usage info
show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE -t {mst,bmst,barch}
Dependency-parse a given .conllx file with a specified parser.

  -h, --help           display this help and exit
  -f, --file   FILE    absolute path to input .conllx file
  -p, --parser PARSER  Dependency parser to be used: 'mst', 'bmst' or 'barch'
EOF
}

is_input_file_set=FALSE
is_parser_set=FALSE

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
        -p|--parser)       # Takes an option argument; ensure it has been specified.
            if [ "$2" ]; then
                is_parser_set=TRUE
                parser=$2
                shift
            else
                die "ERROR: '--parser' requires a non-empty option argument"
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

if [ "${is_parser_set}" = FALSE ]; then
    die "ERROR: '--parser' parameter is required."
fi

case "${parser}" in
    mst )
        ;;   #fallthru
    bmst )
        ;;   #fallthru
    barch )
        ;;   #fallthru
    * )
        die "Invalid dependency parser '${parser}': Should be 'mst', 'bmst' or 'barch'"
esac

prepare_mst_input() {
  local INPUT_FILE=$1
  local OUTPUT_TMP_DIR="/tmp/mst"

  mkdir ${OUTPUT_TMP_DIR} 2> /dev/null

  while read line; do
      echo $line | grep '^$' > /dev/null && echo "" >> ${OUTPUT_TMP_DIR}/mst.tmp
      echo $line | grep '^$' > /dev/null || echo "0" >> ${OUTPUT_TMP_DIR}/mst.tmp
  done < $INPUT_FILE;

  cut -f 1-6 ${INPUT_FILE} > ${OUTPUT_TMP_DIR}/mst.first.to.sixth
  cut -f 8-10 ${INPUT_FILE} > ${OUTPUT_TMP_DIR}/mst.eigth.to.tenth

  paste ${OUTPUT_TMP_DIR}/mst.first.to.sixth ${OUTPUT_TMP_DIR}/mst.tmp ${OUTPUT_TMP_DIR}/mst.eigth.to.tenth | perl -pe "s/^\t+$//g" > ${INPUT_FILE}

  rm -rf $OUTPUT_TMP_DIR
}

convert_mst_to_conllx() {
  local MST_FILE=$1
  local CONLLX_FILE=$2
  local OUTPUT_TMP_DIR="/tmp/mst"

  mkdir ${OUTPUT_TMP_DIR} 2> /dev/null

  cut -f 1-6 ${CONLLX_FILE} > ${OUTPUT_TMP_DIR}/conllx.first.to.sixth
  cut -f 7-8 ${MST_FILE} > ${OUTPUT_TMP_DIR}/mst.seventh.to.eigth
  cut -f 9-10 ${CONLLX_FILE} > ${OUTPUT_TMP_DIR}/ninth.to.tenth

  paste ${OUTPUT_TMP_DIR}/conllx.first.to.sixth ${OUTPUT_TMP_DIR}/mst.seventh.to.eigth ${OUTPUT_TMP_DIR}/ninth.to.tenth | perl -pe "s/^\t+$//g" > ${CONLLX_FILE}

  rm ${MST_FILE}
  rm -rf $OUTPUT_TMP_DIR
}

echo "Initializing dependency parsing..."

if [ "${parser}" = "mst" ]; then
    echo "Preparing .conllx input for MST parsing..."
    prepare_mst_input $file
    echo "Done"
    echo "Dependency-parsing via MSTParser..."
    pushd ${MST_PARSER_HOME}
    ${JAVA_HOME_BIN}/java \
      -classpath ".:./lib/trove.jar:./lib/mallet-deps.jar:./lib/mallet.jar" \
    	-Xms${min_ram} \
    	-Xmx${max_ram} \
    	mst.DependencyParser \
    	test \
    	separate-lab \
    	model-name:${mst_parser_model} \
    	decode-type:proj \
    	order:2 \
    	test-file:${file} \
    	output-file:${file}.mst \
    	format:CONLL > ${LOGS_DIR}/mst.log
    echo "Done"
    echo "Converting .mst to .conllx..."
    convert_mst_to_conllx ${file}.mst ${file}
    echo "Done"
fi

if [ "${parser}" = "bmst" ]; then
  echo "Dependency-parsing via BIST MST parser..."
  OUTPUT_DIR=$(dirname "${file}")
  python ${BMST_PARSER_HOME}/parser.py \
      --predict \
      --outdir ${OUTPUT_DIR} \
      --test ${file} \
      --extrn ${bist_external_vectors} \
      --model ${bmst_model} \
      --params ${bmst_params} 2> ${LOGS_DIR}/bmst.log
  rm "${OUTPUT_DIR}/test_pred.conll.txt"
  mv "${OUTPUT_DIR}/test_pred.conll" "${file}"
  echo "Done"
fi

if [ "${parser}" = "barch" ]; then
  echo "Dependency-parsing via BIST ARCH parser..."
  OUTPUT_DIR=$(dirname "${file}")
  python ${BARCH_PARSER_HOME}/parser.py \
      --predict \
      --outdir ${OUTPUT_DIR} \
      --test ${file} \
      --extrn ${bist_external_vectors} \
      --model ${barch_model} \
      --params ${barch_params} 2> ${LOGS_DIR}/barch.log
  rm "${OUTPUT_DIR}/test_pred.conll.txt"
  mv "${OUTPUT_DIR}/test_pred.conll" "${file}"
  echo "Done"
fi
