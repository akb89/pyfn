#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE -t {mxpost,nlp4j}
Part-of-speech tag a given .sentences file with a specified tagger.

  -h, --help                   display this help and exit
  -f, --file   FILE            absolute path to input .sentences file
  -t, --tagger {mxpost,nlp4j}  pos tagger to be used: 'mxpost' or 'nlp4j'
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
        -f|--file)
            if [ "$2" ]; then
                is_input_file_set=TRUE
                file=$2
                shift
            else
                die "ERROR: '--file' requires a non-empty option argument"
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
        die "Invalid pos tagger '${tagger}': Should be 'mxpost' or 'nlp4j'"
esac

echo "Initializing part-of-speech tagging..."

mkdir ${LOGS_DIR} 2> /dev/null

if [ "${tagger}" = "mxpost" ]; then
    echo "POS tagging via MXPOST..."
    pushd ${MXPOST_HOME}
    echo "Processing file: ${file}"
    echo "Masking _ chars..."
    python3 ${SCRIPTS_DIR}/CoNLLizer.py mask -m "ùé$" -s "_" ${file} > ${file}.masked
    echo "Done"
    echo "POS tagging masked file..."
    ./mxpost tagger.project < ${file}.masked > ${file}.mxpost 2> ${LOGS_DIR}/mxpost.log
    echo "Done"
    echo "Processing file: ${file}.mxpost"
    echo "Brownifying..."
    python3 ${SCRIPTS_DIR}/CoNLLizer.py brown -i ${file}.mxpost > ${file}.mxpost.conll.tmp
    echo "Done"
    echo "Unmasking _ chars..."
    python3 ${SCRIPTS_DIR}/CoNLLizer.py unmask -c -f 2 -m "ùé$" -s "_" ${file}.mxpost.conll.tmp > ${file}.mxpost.conll.tmp.unmasked
    echo "Done"
    echo "Converting .mxpost file to .conllx format..."
    python3 ${SCRIPTS_DIR}/CoNLLizer.py conll -f 1,2,4,3,3,4,4,4,4,4 -r 4 -w _ ${file}.mxpost.conll.tmp.unmasked ${file}.mxpost.conll.tmp.unmasked > ${file}.conllx
    # rm ${file}.mxpost.conll.tmp
    # rm ${file}.mxpost
    echo "Done"
fi

if [ "${tagger}" = "nlp4j" ]; then
    echo "Converting .sentences to .tsv format..."
    echo "Processing file: ${file}"
    python3 ${SCRIPTS_DIR}/CoNLLizer.py mask -m "ùé$" -s "_"
    python3 ${SCRIPTS_DIR}/CoNLLizer.py brown -i ${file} > ${file}.tsv.tmp
    python3 ${SCRIPTS_DIR}/CoNLLizer.py unmask -c -f 2 -m "ùé$" -s "_"
    python3 ${SCRIPTS_DIR}/CoNLLizer.py conll -f 1,2,3,3,3,3,3,3,3 -r 3 -w _ ${file}.tsv.tmp ${file}.tsv.tmp > ${file}.tsv
    rm ${file}.tsv.tmp
    echo "Done"
    echo "POS tagging via NLP4J..."
    echo "Processing file: ${file}.tsv"
    sh ${NLP4J_HOME}/bin/nlpdecode \
      -c ${nlp4j_config} \
      -format tsv \
      -i ${file}.tsv \
      -oe nlp4j \
      -threads ${num_threads} > ${LOGS_DIR}/nlp4j.log
    echo "Done"
    echo "Converting .nlp4j to .conllx format..."
    echo "Processing file: ${file}.tsv.nlp4j"
    python3 ${SCRIPTS_DIR}/CoNLLizer.py conll -f 1,2,3,4,4,5,5,5,5,5 -r 5 -w _ ${file}.tsv.nlp4j ${file}.tsv.nlp4j > ${file}.conllx
    rm ${file}.tsv
    rm ${file}.tsv.nlp4j
    echo "Done"
fi
