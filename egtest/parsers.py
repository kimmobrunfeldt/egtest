"""
Text parsers.
"""

from collections import namedtuple
import re


CodeInfo = namedtuple('Code', ['command', 'code'])


class GitHubMarkdownParser(object):

    regex = re.compile('```(.*?)```', re.DOTALL)

    def __init__(self, text):
        self._text = text

    def blocks(self):
        """Parses code blocks from given text and returns them as a list of
        unicode strings.
        """
        matches = re.findall(self.regex, self._text)
        codes = []
        for match in matches:
            code_info = CodeInfo(
                command=self._find_command(match),
                code=self._clean_block(match)
            )
            codes.append(code_info)

        return codes

    def _find_command(self, block):
        """Finds language of code block"""
        block = block.strip()
        start_tag = block.split('\n', 1).strip()
        if start_tag == '```':
            return None

        return block[len('```'):]

    def _clean_block(self, block):
        """Cleans single block match text from surrounding markdown syntax."""
        block = block.strip()
        # Remove first line: ```<language>
        # and last line: ```
        return '\n'.join(block.splitlines()[1:-1])

    def _remove_indentation(self, text):
        """Removes extra indentation from text block. Indentation of first text
        line is counted as 'extra'.
        """
        lines = text.splitlines()
        indentation = len(lines[0]) - len(lines[0].lstrip())
        indent_string = lines[0][:indentation]

        new_lines = []
        for line in lines:
            if line.startswith(indent_string):
                line = line[indentation:]

            new_lines.append(line)

        return '\n'.join(new_lines)


# List all available parsers for config-friendly usage
available = {
    'github_markdown': GitHubMarkdownParser
}
