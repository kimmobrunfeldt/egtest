# E.g. test

[![Build Status](https://travis-ci.org/kimmobrunfeldt/egtest.png?branch=master)](https://travis-ci.org/kimmobrunfeldt/egtest)
[![Coverage Status](https://coveralls.io/repos/kimmobrunfeldt/egtest/badge.png?branch=master)](https://coveralls.io/r/kimmobrunfeldt/egtest?branch=master)
[![Badge fury](https://badge.fury.io/py/egtest.png)](https://badge.fury.io/py/egtest.png)
[![Badge PyPi](https://pypip.in/d/egtest/badge.png)](https://pypip.in/d/egtest/badge.png)

*E.g. test* parses code blocks from documentation, runs them and reports possible errors. Incorrect example is worse than no example at all. Your examples can be written in any language.

**Example**

Python code block, which tries to demonstrate printing

```python
# We have syntax error in the example
print('This is how you print a line)
```

Running `egtest README.md` looks like this:

![screenshot](docs/screenshot.png)

*E.g. test* supports piping, reporting in JSON format and everything needed to integrate with other tools. Check out [detailed usage](#detailed-usage).

## Install

You'll need Python to run egtest. Python versions 2.6, 2.7 and 3.3 are supported and tested against.

Install latest release with *pip*:

    pip install egtest

Install latest development version usin *pip*:

    pip install git+git://github.com/kimmobrunfeldt/egtest.git

Install latest development version using *setup.py*:

    git clone git@github.com:kimmobrunfeldt/egtest.git
    cd egtest
    python setup.py install

## Detailed usage

Code examples are written into temporary files. They are run with command parsed from code block, and if the temporary code exits with non-zero return value, *egtest* reports errors.

Output of `egtest --help`

    E.g. test - Test example code blocks in documentation

    Usage:
      egtest [<filename>] [--reporter=<reporter>] [--parser=<parser>] [--config=<config>]
      egtest -h | --help
      egtest --version

    Examples:
      egtest readme.md
      egtest --reporter json readme.md
      cat readme.md | egtest
      egtest < readme.md

    Options:
      -r --reporter=<reporter>  Sets reporter. Valid values: basic, json.
      -p --parser=<parser>      Sets parser. Valid values: markdown.
      -c --config=<config>      External configuration. File path to config JSON.
      -h --help                 Show this screen.
      -v --version              Show version.

You can use external JSON file along with command line parameters to control egtest. Check [example-config.json](docs/example-config.json).

### Reporters

*E.g. test* supports two different reporter types: *basic* and *json*.

When JSON reporter is used, *egtest* outputs results in JSON format. For example `egtest --reporter json README.md | python -m json.tool` outputs:

```json
{
    "executions": [
        {
            "code": "# We have syntax error in the example\nprint('This is how you print a line)",
            "command": "python",
            "output": {
                "returnValue": 1,
                "stderr": "  File \"/var/folders/2l/qmg1cgh90h1fdzjcdp9_ss580000gp/T/tmpOJfmPa\", line 6\n    print('This is how you print a line)\n                                       ^\nSyntaxError: EOL while scanning string literal\n",
                "stdout": ""
            }
        }
    ]
}
```

### Parsers

Parser reads documentation in text format and extracts all code examples including what command should be used to run them.

Currently only one format is supported, which is GitHub's markdown. It parses only [fenced code blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code-and-syntax-highlighting) to extract the language of code.

### Injecting code

It is possible to define custom code which will be injected on each example before running. For Python code, *egtest* adds current working directory to *sys.path* to make imports possible.

*Currently there's no sensible way to add custom injections without modifying [egtest/injecthooks.py](egtest/injecthooks.py).*

## Contributing

[Documentation for Egtest developers](docs/)
