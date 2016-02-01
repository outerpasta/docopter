from os.path import realpath, join, dirname, basename
from os import listdir
import imp

from docopt import DocoptLanguageError, DocoptExit
from docopt import parse_section, parse_pattern, parse_defaults
from docopt import formal_usage
from docopt import Required, Either, OneOrMore, Optional
from docopt import Option, Command, Argument
from docopt import OptionsShortcut

from re import sub, match, search, MULTILINE, DOTALL


class DocLoader():
    def __init__(self, scripts_dir=join(dirname(__file__), 'scripts')):
        self.SCRIPTS_DIR = scripts_dir
        self.scripts = self.load()

    def load(self):
        scripts = []
        for script in listdir(self.SCRIPTS_DIR):
            path = realpath(join(self.SCRIPTS_DIR, script))
            if path.endswith('.py'):
                scripts.append(self.create_console(imp.load_source(script.split('.py')[0], path)))
            elif path.endswith('.sh'):

                def bash_script():
                    pass

                with open(path, 'r') as f:
                    text = f.read()
                # try:
                bash_script.__setattr__("__doc__", search('EOF.+EOF', text, DOTALL|MULTILINE).group()[3:-3])
                # except:
                #     continue

                bash_script.__setattr__("__name__", sub('\.sh', '', basename(path)))
                bash_script.__setattr__("__file__", path)
                scripts.append(self.create_console(bash_script))
            else:
                pass
        return scripts

    def create_console(self, script):
        usage_sections = parse_section('usage:', script.__doc__)
        if len(usage_sections) == 0:
            raise DocoptLanguageError('"usage:" (case-insensitive) not found.')
        if len(usage_sections) > 1:
            raise DocoptLanguageError('More than one "usage:" (case-insensitive).')
        DocoptExit.usage = usage_sections[0]
        pattern = parse_pattern(formal_usage(DocoptExit.usage), parse_defaults(script.__doc__))

        paths = []

        paths.append({
            "flags": [opt for opt in parse_defaults(script.__doc__) if not opt.argcount and opt.name not in ["--help", "--version"]],
            "extras": [opt for opt in parse_defaults(script.__doc__) if not opt.argcount and opt.name in ["--help", "--version"]],
            "options": [opt for opt in parse_defaults(script.__doc__) if opt.argcount and not opt.value],
            "default_options": [opt for opt in parse_defaults(script.__doc__) if opt.value],
            "arguments": [arg.name for arg in pattern.flat(Argument)],
        })

        return {
            "name": script.__name__,
            "file": script.__file__,
            "doc": script.__doc__,
            "paths": paths,
        }

        # def walk_tree(p, tab='', r=[]):
        #     if hasattr(p, 'children'):
        #         # print tab, sub("'>", '', sub('.*docopt\.', '', str(type(p))))
        #         r.append(p)
        #         for child in p.children:
        #             walk_tree(child, tab + ' + ')
        #     else:
        #         print tab, p, p.name
        #
        # # walk_tree(pattern.children[0])
        # for child in pattern.children[0].children:
        #     print walk_tree(child)

        # print '\n'

if __name__ == "__main__":
    from pprint import pprint
    b = DocLoader()

    pprint(b.scripts)
