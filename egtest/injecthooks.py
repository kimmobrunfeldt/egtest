"""
All injectors.
"""

import os

from .parsers import CodeInfo


def should_inject_custom(code_info):
    """Returns True if the code looks like suitable to inject our custom
    stuff into it.
    """
    return code_info.command == 'custom'


def inject_custom(code_info):
    return code_info


def inject_python(code_info):
    """Injects code snippet in python code"""
    cwd = os.getcwd()
    append = u'# Injected by egtest\n'
    append += u'import sys\n'
    append += u'sys.path.insert(0, "%s")\n\n' % cwd
    append += code_info.code
    return append


def inject_all(code_info):
    """Executes all matching injectors."""

    new_code_info = CodeInfo(code_info.command, code_info.code)
    for decision, inject_func in hooks:

        if hasattr(decision, '__call__'):
            # It is a function
            should_inject = decision(code_info)
        else:
            should_inject = code_info.command == decision

        if should_inject:
            new_code = inject_func(new_code_info)
            new_code_info.code = new_code

    return new_code_info


# Code which should be injected to each example
# First object can be either function to decide if the injection should be done,
# or str which is name of egtest.parsers.CodeInfo.command to be matched.
# Injectors are executed in the order of list
hooks = [
    (should_inject_custom, inject_custom),
    ('python', inject_python)
]
