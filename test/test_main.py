"""
Tests for main program.
"""

import unittest

import egtest.utils as utils


class TestMain(unittest.TestCase):

    def test_multiple_invalid(self):
        ret, out, err = self._run('multiple-invalid.md')
        print out, err
        self.assertEquals(ret, 2, 'egtest exited with incorrect value')



    def _run(filename, params=''):
        """Run egtest for test/<filename> with given parameters."""
        cmd = [
            'python',
            'main.py'
        ]
        cmd += params.split()
        cmd.append('test/%s' % filename)

        return utils.run_command(cmd)
