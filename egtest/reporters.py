"""
Text parsers.
"""

from colorama import Fore, Style
from colorama import init
init(autoreset=True)

from utils import indent


class ExecInfo(object):
    def __init__(self, return_value, stdout, stderr):
        self.return_value = return_value
        self.stdout = stdout
        self.stderr = stderr


class BasicReporter(object):

    def report(self, code_info, exec_info):
        """Outputs execution information to user."""
        if exec_info.return_value != 0:
            print(Fore.RED + 'Error executing code:\n')
            print(Style.BRIGHT + indent(code_info.code.encode('utf-8')))
            print('')
            print(Fore.GREEN + 'stdout:')
            print(exec_info.stdout)
            print(Fore.RED + 'stderr:')
            print(exec_info.stderr)


# List all available parsers for config-friendly usage
available = {
    'basic': BasicReporter,
    # For example:
    # 'json': JsonReporter,
}
