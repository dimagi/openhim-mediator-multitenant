#!/usr/bin/env python
"""
Renders STDIN using environment variables as context

    $ echo "Ghost in the {{ SHELL }}" | render-env.py
    Ghost in the /usr/bin/zsh

"""
import fileinput
import os
from jinja2 import Template


if __name__ == '__main__':
    string = ''.join(fileinput.input())
    template = Template(string)
    print(template.render(os.environ))
