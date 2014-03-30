# -*- encoding: utf-8 -*-
"""
Integration tests for main program.

Note: These tests are not included to coverage.
It would be possible, by importing main and running main function from the
tests but catching stdout and sys.exit() calls is semi-hack.
Though these tests are not very clean anyways.
"""

import json
import unittest
from subprocess import Popen, PIPE

from egtest import utils


class TestMain(unittest.TestCase):
    """Tests for main.py"""

    def test_multiple_invalid(self):
        ret, out, err = self._run('test/multiple-invalid.md', json_report=True)
        self.assertEqual(ret, 2, 'egtest exited with incorrect value')

        executions = out['executions']
        failures = self._find_failures(executions)
        self.assertEqual(len(failures), 2, 'incorrect amount of failures')

    def test_invalid_external_config(self):
        cmd = '--config test/invalid-config.json test/valid.md'
        ret, out, err = self._run(cmd)
        self.assertNotEqual(ret, 0, 'invalid json did not fail')

    def test_parameters_override(self):
        """Default parameters are overridden by external config and both
        are overridden by command line arguments.
        """
        # First we set invalid external config
        cmd = '--config test/invalid-config.json -p markdown test/valid.md'
        ret, out, err = self._run(cmd)
        self.assertEqual(ret, 0, 'parameter overriding did not work')

    def test_valid(self):
        ret, out, err = self._run('test/valid.md')
        self.assertEqual(ret, 0, 'very simple valid example failed')

    def test_config_validation(self):
        ret, out, err = self._run('--parser notexist test/valid.md')
        self.assertNotEqual(ret, 0, 'egtest accepted invalid parser')

        ret, out, err = self._run('--reporter notexist test/valid.md')
        self.assertNotEqual(ret, 0, 'egtest accepted invalid reporter')

    def test_specialchars(self):
        ret, report, err = self._run('test/specialchars.md', json_report=True)
        self.assertEqual(ret, 0, 'example with special chars failed')

        # Take the actual output what egtest reported
        run_out = report['executions'][0]['output']['stdout']
        self.assertEqual(run_out, u'汉语漢', 'special chars reading failed')

    def test_piping(self):
        cmd = self._get_cmd('', json_report=True)
        p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE)

        text = utils.read_file('test/specialchars.md')
        stdout_data = p.communicate(input=text.encode('utf-8'))[0]
        stdout = stdout_data.decode('utf-8')
        run_out = json.loads(stdout)['executions'][0]['output']['stdout']
        self.assertEqual(run_out, u'汉语漢', 'special chars piping failed')

    def _find_failures(self, executions):
        failures = []
        for ex in executions:
            if ex['output']['returnValue'] > 0:
                failures.append(ex)

        return failures

    def _run(self, params, json_report=False):
        """Run egtest in as sub process"""
        cmd = self._get_cmd(params, json_report)
        ret, out, err = utils.run_command(cmd)

        if json_report:
            out = json.loads(out)

        return ret, out, err

    def _get_cmd(self, params, json_report):
        """Return Popen format command for running egtest."""
        cmd = [
            'python',
            '-m'
            'egtest.main'
        ]
        cmd += params.split()
        if json_report:
            cmd += ['--reporter', 'json']

        return cmd
