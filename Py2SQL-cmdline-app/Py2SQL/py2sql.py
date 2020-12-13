# -*- coding: utf-8 -*-


"""Py2SQL.py2sql: provides entry point main()."""

__version__ = "0.2.1"

import os
import sqlite3
import sys
from typing import *
from config import *

class Database:
    def _set_constants(self):
        pass

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        pass

    def _db_connect(self):
        """
            Установка подключения
        :return: sqlite3.Connection или же объект подключения
        """
        return sqlite3.connect(database=DB_FILENAME)

    def _db_disconnect(self):
        """
            Закрываем подключение и все курсоры.
        :return:
        """
        self._cursor.close()
        self._connect.close()



def main():
    print("Executing Py2SQL version %s." % __version__)