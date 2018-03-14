#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -f FILE
Flatten .conllx file to SEMAFOR .all.lemma.tags file.

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

echo "Converting to .flattened format for the SEMAFOR parser..."
echo "Processing file: ${file}"
python3 CoNLLizer.py flatten -c -f 2,4,8,7,5,3 -r 5 -w O ${file} > ${file}.flattened
