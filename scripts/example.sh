#!/bin/bash
# See http://docopt.org/ for more info on docopt usage
eval "$(python $(dirname ${BASH_SOURCE[0]})/docopts -V - -h - : "$@" <<EOF
Usage: example [options] <env>

      -a --advance=NEW_VALUE        Advance [default: 0]
      --verbose
                         Generate verbose messages.
      -h --help                     Show help options.
      --version                     Print program version.

----
example 0.1.0
EOF
)"

echo "$env"
