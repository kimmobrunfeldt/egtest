#!/usr/bin/env python

"""E.g. test - Test example code blocks in documentation

Usage:
  egtest [<filename>]
  egtest -h | --help
  egtest --version

Examples:
  egtest readme.md
  cat readme.md | egtest

Options:
  -h --help                 Show this screen.
  -v --version              Show version.
"""

import os
import sys
import tempfile

from egtest import injecthooks, parsers, reporters, utils, __version__

_PY3 = sys.version_info >= (3, 0)


config = {
    # All parsers in egtest.parsers.available dict
    'parser': 'github_markdown',

    # All reporters in egtest.reporters.available dict
    'reporter': 'basic'
}

def main():
    from docopt import docopt
    arguments = docopt(
        __doc__,
        argv=sys.argv[1:],
        help=True,
        version=__version__
    )

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


def run_code_blocks(text):
    Parser = parsers.available[config['parser']]
    parser = Parser(text)

    blocks = parser.blocks()

    Reporter = reporters.available[config['reporter']]
    reporter = Reporter(blocks)

    exec_infos = []
    for code_info in blocks:
        exec_info = run_code_block(code_info)
        exec_infos.append(exec_info)

        reporter.on_execute(code_info, exec_info)

    # If any of return values != 0 -> failure
    success = not any([info.return_value for info in exec_infos])
    reporter.on_finish(exec_infos, success)

    return success


def run_code_block(code_info):
    new_code_info = injecthooks.inject_all(code_info)
    exec_info = run_code(new_code_info)
    return exec_info


def run_code(code_info):
    f, abspath = tempfile.mkstemp(text=True)
    utils.write_file(code_info.code, abspath)
    ret_val, stdout, stderr = utils.run_command([code_info.command, abspath])
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
        print('KeyboardInterrupt')
