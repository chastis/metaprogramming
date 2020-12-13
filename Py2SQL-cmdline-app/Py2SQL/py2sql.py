# -*- coding: utf-8 -*-


"""Py2SQL.py2sql: provides entry point main()."""

__version__ = "0.2.1"

import os
import sqlite3
import sys
from typing import *

import Py2SQL.util_for_db as util
import Py2SQL.util_for_handle_usual_data as handler
from config import *
from Py2SQL import sql_queries


class Car:
    def __init__(self, color: str = 'RED', number: int = 5, title: str = "BMW"):
        self.color = color
        self.number = number
        self.title = title


class Database:
    def _set_constants(self):
        """
         Устанавливаем в классовые переменные инфу о базе и версии используемого API.
         :return:
        """
        self._db_name: str = DB_FILENAME.split('.')[0]
        self._db_version: str = sqlite3.version
        self._db_sqlite_version: str = sqlite3.sqlite_version
        self._db_engine: str = 'SQLite3: ' + self._db_version
        self._db_size: int = self._db_get_size()

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

    # def __del__(self):
    #     """
    #     Реализация деструктора, удаление курсора и коннекшина.
    #     :return:
    #     """
    #
    #     self._db_disconnect()

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

    def _db_get_size(self) -> int:
        return os.path.getsize(filename=DB_FILENAME) / (1024 ** 2) if os.path.exists(DB_FILENAME) else 0

    def _execute(self, queries: Union[Tuple, List, Set, FrozenSet, str, None]):
        if isinstance(queries, str):
            queries = (queries,)

        for query in queries:
            self._cursor.execute(query)

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
            self._execute(queries=queries)
        self._connect.commit()

    def get_tables(self) -> tuple:
        self._cursor.execute(sql_queries.GET_TABLES)
        return util.output_one_column(data=self._cursor.fetchall())

    def get_table_info(self, table: str) -> list:
        """
        :param table: название таблицы в БД
        :return: список параметров таблицы: айди_поля, название_поля, тип_поля.
        """
        self._cursor.execute(sql_queries.GET_TABLE_INFO(table=table))
        # return util.table_info(title_columns=self._cursor.description,
        #                        data=self._cursor.fetchall())
        return self._cursor.fetchall()

    def find_object(self, table: str, py_object: object) -> list:
        """
            Поиск строки с эквивалетными параметрами что и у объекта
        :param table: название таблицы
        :param py_object: объект требуемый к нахождению
        :return: список кортежей где 1 кортеж является информацией о одном поле
        """
        if table in self.get_tables():
            query: str = util.generate_sql_to_find_object(table=table,
                                                          attributes=tuple(py_object.__dict__.items()))
            table_fields: List[Tuple] = self.get_table_info(table=table)
            self._execute(queries=query)
            return handler.merge_field_info_with_value(fields_info=table_fields,
                                                       data=self._cursor.fetchall())

        else:
            raise Exception('Введенной таблицы не найдено.')

    def find_objects_by(self, table: str, *attributes):
        """
            Поиск записи по заданным параметрам
        :param table: название таблицы
        :param attributes: нужный параметры для поиска
        :return: найденные строки в формате: название стобца, тип, занчение
        """
        if table in self.get_tables():
            query: str = util.generate_sql_to_find_object(table=table,
                                                          attributes=tuple(attributes)[0])
            table_fields: List[Tuple] = self.get_table_info(table=table)
            self._execute(queries=query)
            return handler.merge_field_info_with_value(fields_info=table_fields,
                                                       data=self._cursor.fetchall())
        else:
            raise Exception('Введенной таблицы не найдено.')

    def find_class(self, py_class):
        pass


def main():
    print("Executing Py2SQL version %s." % __version__)
    with Database() as db:
        print(db.find_objects_by('car', (("color", "RED"), ("number", 5))))
        # print(db.find_object('car', Car()))
        # print(db.get_table_info('asdasdasdasd'))
