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
        """
         Устанавливаем в классовые переменные инфу о базе и версии используемого API.
         :return:
        """
        self._db_name: str = DB_FILENAME.split('.')[0]
        self._db_version: str = sqlite3.version
        self._db_sqlite_version: str = sqlite3.sqlite_version

    def __init__(self):
        """
        Конструктор для класса, производится коннект и получение курсора
        """

        self._set_constants()

        self._connect: sqlite3.Connection = self._db_connect()
        self._cursor: sqlite3.Cursor = self._connect.cursor()

    def __enter__(self):
        """
        Реализовано для менеджера контекста (with as)
        :return: объект базы данных
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Реализовано для менеджера контекста (with as)
        :return:
        """

        self._db_disconnect()

    def __del__(self):
        """
        Реализация деструктора, удаление курсора и коннекшина.
        :return:
        """

        self._db_disconnect()

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

    def _commit(self, queries: Union[Tuple, List, Set, FrozenSet, str, None]):
        """
        Функция для закрепления транзакции, для уменьшения количества строк кода.
        :param queries: запросы, может быть как один запрос в виде строки,
                        так и несколько в какой-либо форме list/set/tuple
        :return:
        """

        if queries:
            if isinstance(queries, str):
                queries = (queries,)

            for query in queries:
                self._cursor.execute(query)
        self._connect.commit()


def main():
    print("Executing Py2SQL version %s." % __version__)
    Database()