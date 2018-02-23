#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XPDIR -u
Train or decode with the OPEN-SESAME parser.

  -h, --help                          display this help and exit
  -m, --mode          {train,decode}  rofames mode to use: train or decode
  -x, --xpdir         XPDIR           absolute path to the xp directory (where data/ and model/ will be stored)
  -u, --use_hierarchy                 if specified, parser will use the hierarchy feature
EOF
}
