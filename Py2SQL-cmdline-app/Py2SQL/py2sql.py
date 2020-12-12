# -*- coding: utf-8 -*-


"""Py2SQL.py2sql: provides entry point main()."""

__version__ = "0.2.0"

import sys


def main():
    print("Executing bootstrap version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])