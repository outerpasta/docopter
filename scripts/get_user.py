"""Get User Script.
Usage:
  get_user [options] <env> <email>

Options:
  --level=VALUE   print a list [default: 0]
  --cat=VALUE     print a cat
  -h --help       Show this screen.
  --version       Show version.
"""
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print args