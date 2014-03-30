#!/usr/bin/env python

"""E.g. test - Test example code blocks in documentation

Usage:
  egtest [<filename>] [--reporter=<reporter>] [--parser=<parser>] [--config=<config>]
  egtest -h | --help
  egtest --version

Examples:
  egtest readme.md
  egtest --reporter json readme.md
  cat readme.md | egtest
  egtest < readme.md

Options:
  -r --reporter=<reporter>  Sets reporter. Valid values: basic, json.
  -p --parser=<parser>      Sets parser. Valid values: markdown.
  -c --config=<config>      External configuration. File path to config JSON.
  -h --help                 Show this screen.
  -v --version              Show version.
"""

import json
import os
import sys
import tempfile

import six

from egtest import injecthooks, parsers, reporters, utils, __version__


default_config = {
    # All parsers in egtest.parsers.available dict
    'parser': 'markdown',

    # All reporters in egtest.reporters.available dict
    'reporter': 'basic'
}

def main(argv):

    from docopt import docopt
    arguments = docopt(
        __doc__,
        argv=argv,
        help=True,
        version=__version__
    )

    config = combine_configs(arguments)
    validate_config(config)
    text = read_text(config['filename'])
    success = run_code_blocks(config, text)

    if not success:
        sys.exit(2)


def read_text(filename):
    if filename is not None:
        try:
            text = utils.read_file(filename)
        except IOError as e:
            print('Could not open file. %s' % e)
            sys.exit(1)
    else:
        # This makes it possible to use via pipe e.g. x | python egtest.py
        text = sys.stdin.read()
        if six.PY2:
            text = text.decode('utf-8')

    return text


def combine_configs(arguments):
    """Combines all configurations:
    - Default configuration
    - External JSON configuration
    - Commandline arguments

    Lower configuration overrides above configurations.
    """
    config = default_config.copy()

    if '--config' in arguments and arguments['--config']:
        config.update(read_jsonfile(arguments['--config']))

    arguments_config = {
        'reporter': arguments['--reporter'],
        'parser': arguments['--parser'],
        'filename': arguments['<filename>']
    }
    config.update((k, v) for k, v in arguments_config.items()
                  if v is not None or k == 'filename')

    return config


def validate_config(config):
    if config['parser'] not in parsers.available:
        print('No such parser: %s' % config['parser'])
        sys.exit(1)

    if config['reporter'] not in reporters.available:
        print('No such reporter: %s' % config['reporter'])
        sys.exit(1)


def read_jsonfile(file_path):
    return json.loads(open(file_path).read())


def run_code_blocks(config, text):
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
    os.close(f)

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
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
