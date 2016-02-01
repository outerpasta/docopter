#!/usr/bin/env python
"""Get User Script.
Usage:
  get_user [options] <env> <email>

Options:
  --level=VALUE   print a list [default: 0]
  -h --help       Show this screen.
  --version       Show version.
"""
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print args