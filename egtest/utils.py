"""
Generic functions.
"""

import subprocess

import six


def read_file(filepath, encoding='utf-8'):
    """Reads file's contents and returns unicode."""
    open_func = open
    if six.PY3:
        open_func = lambda f, mode: open(f, mode, encoding=encoding)

    with open_func(filepath, 'r') as f:
        content = f.read()

    if not six.PY3:
        content = content.decode(encoding, 'replace')

    return content


def write_file(text, filepath, encoding='utf-8'):
    """Writes unicode to file with specified encoding."""
    open_func = open
    if six.PY3:
        open_func = lambda f, mode: open(f, mode, encoding=encoding)
    else:
        text = text.encode(encoding, 'replace')

    with open_func(filepath, 'w') as f:
        f.write(text)


def run_command(command):
    """Runs an command and returns the stdout and stderr as a string.

    Args:
        command: Command to execute in Popen's list format.
                 E.g. ['ls', '..']

    Returns:
        tuple. (return_value, stdout, stderr), where return_value is the
        numerical exit code of process and stdout/err are strings containing
        the output. stdout/err is None if nothing has been output.
    """
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return_value = p.wait()
    return return_value, stdout.decode('utf-8'), stderr.decode('utf-8')


def indent(text, indent=4):
    """Indents text with spaces."""
    return u'\n'.join([u' ' * indent + x for x in text.splitlines()])
