"""
Text parsers.
"""

from __future__ import print_function
import six
print = six.print_

import json

from colorama import Fore, Style
from colorama import init
init(autoreset=True)

from .utils import indent


class ExecInfo(object):
    def __init__(self, return_value, stdout, stderr):
        self.return_value = return_value
        self.stdout = stdout
        self.stderr = stderr


class BasicReporter(object):

    def __init__(self, blocks):
        """
        blocks: code blocks to be executed
        """
        self._blocks = blocks
        print('Testing %s example(s)..\n' % len(self._blocks))

    def on_execute(self, code_info, exec_info):
        """
        Outputs execution information to user.
        """
        if exec_info.return_value != 0:
            print('%s---------------------\n' % Style.BRIGHT)
            print('%sError executing code:\n' % Fore.RED)
            print(u'{0}{1}\n'.format(
                Style.BRIGHT,
                indent(code_info.code)
            ))
            print('%sstdout:' % Fore.GREEN)
            print(exec_info.stdout)
            print('%sstderr:' % Fore.RED)
            print(exec_info.stderr)

    def on_finish(self, exec_infos, success):
        """
        exec_infos: List of ExecInfo objects. Contains all executions.
        """
        if success:
            print(Fore.GREEN + '\nSUCCESS')
        else:
            print(Fore.RED + '\nFAILURE')


class JsonReporter(object):

    def __init__(self, blocks):
        """
        blocks: code blocks to be executed
        """
        self._blocks = blocks
        self._json = {
            'executions': []
        }

    def on_execute(self, code_info, exec_info):
        execution = {
            'command': code_info.command,
            'output': {
                'returnValue': exec_info.return_value,
                'stdout': exec_info.stdout,
                'stderr': exec_info.stderr
            },
            'code': code_info.code
        }
        self._json['executions'].append(execution)


    def on_finish(self, exec_infos, success):
        print(json.dumps(self._json))


# List all available parsers for config-friendly usage
available = {
    'basic': BasicReporter,
    'json': JsonReporter
}
