"""
Text parsers.
"""

import re


class CodeInfo(object):
    def __init__(self, command, code):
        self.command = command
        self.code = code


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
        splitted = block.split(u'\n', 1)
        if not splitted[0]:
            return None

        return splitted[0].strip()

    def _clean_block(self, block):
        """Cleans single block match text from surrounding markdown syntax."""
        splitted = block.split(u'\n', 1)

        if len(splitted) < 2:
            return block

        return splitted[1].strip()


# List all available parsers for config-friendly usage
available = {
    'markdown': GitHubMarkdownParser
}
