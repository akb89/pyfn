#!/bin/bash

source "$(dirname "${BASH_SOURCE[0]}")/setup.sh"

show_help() {
cat << EOF
Usage: ${0##*/} [-h] -m {train,decode} -x XPDIR [-s {dev,test}] [-d] [-u]
Train or decode with the OPEN-SESAME parser.

  -h, --help                          display this help and exit
  -m, --mode          {train,decode}  open-sesame mode to use: train or decode
  -x, --xpdir         XPDIR           absolute path to the xp directory (where data/ and model/ will be stored)
  -s, --splits        {dev,test}      which splits to use in decode mode: dev or test
  -d, --dep                           if specified, parser will use dependency parses
  -u, --use_hierarchy                 if specified, parser will use the hierarchy feature
EOF
}
