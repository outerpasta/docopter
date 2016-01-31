"""Get Token.
Usage:
  get_token [<env>]
"""
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    print args