#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XPDIR -u -t {mxpost,nlp4j}
Train or decode with the ROFAMES parser.

  -h, --help                          display this help and exit
  -m, --mode          {train,decode}  rofames mode to use: train or decode
  -x, --xpdir         XPDIR           absolute path to the xp directory (where data/ and model/ will be stored)
  -u, --use_hierarchy                 if specified, parser will use the hierarchy feature
  -t, --tagger        {mxpost,nlp4j}  the POS tagger used for preprocessing splits (used for decoding only)
EOF
}

is_mode_set=FALSE

while :; do
    case $1 in
        -h|-\?|--help)
            show_help
            exit
            ;;
        -m|--mode)
            if [ "$2" ]; then
                is_mode_set=TRUE
                mode=$2
                shift
            else
                die "ERROR: '--mode' requires a non-empty option argument"
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
