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
import sys
import tempfile

from colorama import init
init(autoreset=True)

import injectors
import parsers
import reporters
import utils

_PY3 = sys.version_info >= (3, 0)


config = {
    # All parsers in egtest.parsers.available dict
    'parser': 'github_markdown',

    # All reporters in egtest.reporters.available dict
    'reporter': 'basic',

    # Commands to execute before running code block
    'before': ['']
}

def main():
    from docopt import docopt
    arguments = docopt(__doc__, argv=sys.argv[1:], help=True)

    # Read examples from whatever source

    filename = arguments['<filename>']
    if filename is not None:
        try:
            text = utils.read_file(filename)
        except IOError as e:
            print('Could not open file. %s' % e)
            sys.exit(1)
    else:
        # This makes it possible to use via pipe e.g. x | python egtest.py
        text = sys.stdin.read()

    success = run_code_blocks(text)

    if not success:
        sys.exit(2)
        print('\nExample(s) failed')
    else:
        print('Example(s) passed')


def run_code_blocks(text):
    Parser = parsers.available[config['parser']]
    parser = Parser(text)

    blocks = parser.blocks()
    print('Testing %s example(s)..\n' % len(blocks))

    exec_infos = []
    for code_info in blocks:
        exec_info = run_code_block(code_info)
        exec_infos.append(exec_info)

    # If any of return values != 0 -> failure
    return not any([info.return_value for info in exec_infos])


def run_code_block(code_info):
    new_code_info = injectors.inject_all(code_info)

    exec_info = run_code(code)
    return exec_info


def run_code(code_info):
    f, abspath = tempfile.mkstemp(text=True)
    utils.write_file(code, abspath)
    ret_val, stdout, stderr = run_command([code_info.command, abspath])
    exec_info = reporters.ExecInfo(
        return_value=ret_val,
        stdout=stdout,
        stderr=stderr
    )

    os.remove(abspath)
    return exec_info


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Quit.')
