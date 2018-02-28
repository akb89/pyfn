#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE
Lemmatize a given .conllx file with NLP4J.

  -h, --help           display this help and exit
  -f, --file   FILE    absolute path to input .conllx file
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

mkdir ${LOGS_DIR} 2> /dev/null

echo "Lemmatizing with NLP4J..."
echo "Processing file: ${file}"

sh ${NLP4J_HOME}/bin/nlpdecode \
  -c ${nlp4j_config} \
  -format tsv \
  -i ${file} \
  -oe nlp4j \
  -threads ${num_threads} > ${LOGS_DIR}/nlp4j.log

python3 ${SCRIPTS_DIR}/CoNLLizer.py conll -f 1-3,13-19 ${file}.nlp4j ${file} > ${file}.lemma

mv ${file}.lemma ${file}
rm ${file}.nlp4j

echo "Done"
