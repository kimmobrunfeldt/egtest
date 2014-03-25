"""
Tests for egtest.parsers.
"""

import unittest

from egtest.parsers import GitHubMarkdownParser


class TestGitHubMarkdownParser(unittest.TestCase):

    def test_block_in_same_line(self):
        text = '```python```'
        parser = GitHubMarkdownParser(text)
        blocks = parser.blocks()
        self.assertEqual(len(blocks), 1, 'invalid amout of blocks')

        cmd = blocks[0].command
        self.assertEqual(cmd, 'python', 'incorrectly parsed language')

    def test_short_block(self):
        text = '```python\n# Only comment\n```'
        parser = GitHubMarkdownParser(text)
        blocks = parser.blocks()
        self.assertEqual(len(blocks), 1, 'invalid amout of blocks')

        cmd = blocks[0].command
        self.assertEqual(cmd, 'python', 'incorrectly parsed language')

        code = blocks[0].code
        self.assertEqual(code, '# Only comment', 'incorrectly parsed code')

    def test_without_language_returns_None(self):
        text = '```\n# Only comment\n```'
        parser = GitHubMarkdownParser(text)
        blocks = parser.blocks()
        self.assertEqual(len(blocks), 1, 'invalid amout of blocks')

        cmd = blocks[0].command
        self.assertEqual(cmd, None, 'incorrectly parsed language')

        code = blocks[0].code
        self.assertEqual(code, '# Only comment', 'incorrectly parsed code')
