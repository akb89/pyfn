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

echo "Merging .conllx content to .bios file for the open-sesame parser..."
echo "Processing .bios file: ${bios}"
echo "Processing .conllx file: ${conllx}"
python3 ${SCRIPTS_DIR}/CoNLLizer.py bios -c ${conllx} -b ${bios} -f b1-3,c3,b5,c4,b7-9,c7,b11,c8,b13-16 > ${bios}.tmp
