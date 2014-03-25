"""
Integration tests for main program.
"""

import contextlib
import json
import sys
import unittest

import main

# TODO: On exception, this raises ValueError: I/O operation on closed file
@contextlib.contextmanager
def capture_stdout():
    from cStringIO import StringIO
    oldout = sys.stdout
    try:
        out = StringIO()
        sys.stdout = out
        yield out
    finally:
        sys.stdout = oldout
        out = out.getvalue()


class TestMain(unittest.TestCase):
    """Tests for main.py"""

    def test_multiple_invalid(self):
        executions = self._run('test/multiple-invalid.md')
        print executions
        self.assertEquals(executions, 2, 'egtest exited with incorrect value')


    def _run(self, params, json_report=True):
        """Convert commandline style parameters to argv format(list)."""
        with capture_stdout() as stdout:
            argv = params.split()
            if json_report:
                argv += ['--reporter', 'json']

            main.main(argv)

        output = stdout
        if json_report:
            output = json.loads(output)

        return output

