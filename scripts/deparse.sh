#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

# Usage info
show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE -t {mst,bmst,barch}
Dependency-parse a given .conllx file with a specified parser.

  -h, --help           display this help and exit
  -f, --file   FILE    absolute path to input .sentences file
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

echo "Initializing dependency parsing..."

if [ "${parser}" = "mst" ]; then
    echo "Dependency-parsing via MSTParser..."

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
  echo "Dependency-parsing via BIST ARCH..."

  echo "Done"
fi
