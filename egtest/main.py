#!/usr/bin/env python

"""E.g. test - Test example code blocks in documentation

Usage:
  egtest.py [<filename>]
  egtest.py -h | --help
  egtest.py --version

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
"""

import os
import re
import sys
import tempfile

from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

import egtest

_PY3 = sys.version_info >= (3, 0)

# Constants
start_tag = '<egtest>'
end_tag = '</egtest>'


def main():
    from docopt import docopt
    arguments = docopt(__doc__, argv=sys.argv[1:], help=True)

    # Read examples from whatever source

    filename = arguments['<filename>']
    if filename is not None:
        try:
            text = egtest.utils.read_file(filename, encoding)
        except IOError as e:
            print('Could not open file. %s' % e)
            sys.exit(1)
    else:
        # This makes it possible to use via pipe e.g. x | python egtest.py
        text = sys.stdin.read()

    success = run_examples(text)

    if not success:
        sys.exit(2)
        print('\nExample(s) failed')
    else:
        print('Example(s) passed')


def run_examples(text):
    regex = re.compile('%s(.*?)%s' % (start_tag, end_tag), re.DOTALL)

    ret_vals = []
    matches = re.findall(regex, text)
    print('Testing %s example(s)..\n' % len(matches))

    for match in matches:
        ret_val = run_example(match)
        ret_vals.append(ret_val)

    # If any of ret_vals != 0 -> failure
    return not any(ret_vals)

def run_example(example):
    code = remove_non_code(example)
    code = remove_indent(code)
    code = inject_path_append(code)

    ret_val, stdout, stderr = run_code(code)
    if ret_val != 0:
        print(Fore.RED + 'Error executing code:\n')
        print(Style.BRIGHT + indent(code.encode('utf-8')))
        print('')
        print(Fore.GREEN + 'stdout:')
        print stdout
        print(Fore.RED + 'stderr:')
        print stderr

    return ret_val


def indent(text, indent=4):
    return '\n'.join([u' ' * indent + x for x in text.splitlines()])

def remove_indent(code):
    lines = code.splitlines()
    indent = len(lines[0]) - len(lines[0].lstrip())
    return '\n'.join([x[indent:] for x in lines])


def inject_path_append(code):
    cwd = os.getcwd()
    append = u'# Injected by egtest\n'
    append += u'import sys\n'
    append += u'sys.path.insert(0, "%s")\n\n' % cwd
    append += code
    return append


def remove_non_code(example):
    example = example.strip()
    # Remove first tag line, ```python
    # also remove ``` and tag end line from end
    return '\n'.join(example.splitlines()[2:-2])


def run_code(code):
    f, abspath = tempfile.mkstemp(suffix='.py', text=True)
    write_file(code, abspath)
    run_return = run_command(['python', abspath])

    os.remove(abspath)
    return run_return



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit.')
