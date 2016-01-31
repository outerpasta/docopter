from os.path import realpath, join, dirname
from os import listdir
import imp
try:
    from IPython import embed
except ImportError:
    pass

from bottle import route, run, template

from docopt import DocoptLanguageError, DocoptExit
from docopt import parse_section, parse_pattern, parse_defaults
from docopt import formal_usage
from docopt import Required, Either, OneOrMore, Optional
from docopt import Option, Command, Argument
from docopt import OptionsShortcut

from re import sub


INDEX_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Docopter</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

  <style>
  input.option {
    color: blue;
  }
  </style>

</head>
<body>
<div class="container-fluid">
  <h2>Scripts:</h2>
    <ul>
      % for script in scripts:

        <!--Script Block-->

        <!--<form style="display:inline-block;>-->
        <a href="javascript:ReverseDisplay('{{script['name']}}doc')"><h3>{{script['name']}}</h3></a>

        <div id="{{script['name']}}doc" style="display:none;">
            <pre>{{script['doc']}}</pre>
        </div>

        <!--Path Block-->
        % for path in script['paths']:

            <form>
                % for arg in path['arguments']:
                  <input type="text" placeholder="{{arg}}">
                % end
                <br>
                % for option in path['default_options']:
                  <span> {{option.name}} </span><div class="option"><input type="text" name="{{option}} value="{{option.value}}""></div>
                % end

                % for option in path['options']:
                  <span> {{option.name}} </span><div class="option"><input type="text" name="{{option}}"></div>
                % end

                % for flag in path['flags']:
                  <span> {{flag.name}} </span><input type="checkbox" name="{{flag}}">
                % end

                %if path['flags']:
                  <br>
                %end

                % for flag in path['extras']:
                  <span> {{flag.name}} </span><input type="checkbox" name="{{flag}}">
                % end

                <br><input type="submit">
            </form>

        % end
        <!--Path Block-->

        <!--<pre>{{script['doc']}}</pre>-->

        <!--<p>{{script['file']}}</p>-->


      % end
    </ul>

</div>
<script type="text/javascript" language="JavaScript">
function HideContent(d) {
document.getElementById(d).style.display = "none";
}
function ShowContent(d) {
document.getElementById(d).style.display = "block";
}
function ReverseDisplay(d) {
if(document.getElementById(d).style.display == "none") { document.getElementById(d).style.display = "block"; }
else { document.getElementById(d).style.display = "none"; }
}
</script>
</body>
</html>
"""

def create_console(script):
    usage_sections = parse_section('usage:', script.__doc__)
    if len(usage_sections) == 0:
        raise DocoptLanguageError('"usage:" (case-insensitive) not found.')
    if len(usage_sections) > 1:
        raise DocoptLanguageError('More than one "usage:" (case-insensitive).')
    DocoptExit.usage = usage_sections[0]
    pattern = parse_pattern(formal_usage(DocoptExit.usage), parse_defaults(script.__doc__))


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


if __name__ == '__main__':
    SCRIPTS_DIR = join(dirname(__file__), 'scripts')
    scripts = []
    for script in listdir(SCRIPTS_DIR):
        path = realpath(join(SCRIPTS_DIR, script))
        if not path.endswith('.pyc'):
            scripts.append(create_console(imp.load_source(script.split('.py')[0], path)))

    @route('/')
    def index():
        return template(INDEX_PAGE, scripts=scripts)

    run(host='localhost', port=8005)