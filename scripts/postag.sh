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

echo "Initializing Part-of-speech tagging..."

if [ "${tagger}" = "mxpost" ]; then
    echo "POS tagging via MXPOST..."
    pushd ${MXPOST_HOME}
    ./mxpost tagger.project < ${file} > ${file}.mxpost 2> ${LOGS_DIR}/mxpost.log
    echo "Done"
    echo "Converting to .conllx format..."
    echo "Done"
fi

if [ "${tagger}" = "nlp4j" ]; then
    echo "Converting to NLP4J input format..."

    echo "Done"
    echo "POS tagging via NLP4J..."
    sh ${NLP4J_HOME}/bin/nlpdecode \
      -c ${nlp4j_config} \
      -format tsv \
      -i ${file}.tsv \
      -oe nlp4j \
      -threads ${num_threads} > ${LOGS_DIR}/nlp4j.log
    echo "Done"
    echo "Converting to .conllx format..."
    echo "Done"
fi
