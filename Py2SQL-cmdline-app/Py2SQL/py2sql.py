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
    color = str
    number = int
    title = str

class Cat:
    def __init__(self, id_=1, name='Барсик'):
        self.id = id_
        self.name = name
    id = 1
    name = 'барсик'

class Database:

    def save_object(self, py_object: object):
        """
            Сохранение объекта в базу данных
        :param py_object: объект
        :return: статус добавления, или же контролируемая ошибка
        """
        need_fields: List[Tuple] = handler.convert_python_types_in_sqlite_types(attributes=tuple(vars(py_object).items()),
                                                                                object_=True)
        tables_list: tuple = self.get_tables()

        for table in tables_list:

            if set(row[1:] for row in self.get_table_info(table)) == set(need_fields):

                try:
                    self._execute(queries=util.check_having_in_table(table=table,
                                                                     id_=py_object.id))
                    update: bool = bool(self._cursor.fetchone())
                except AttributeError:
                    raise Exception(EXCEPTION_TEXT_NO_ID)

                self._commit(queries=util.generate_save_sql_query(table=table,
                                                                  py_object=py_object,
                                                                  update=update))
                return RECORD_UPDATE if update else RECORD_INSERT

        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS)

    def save_class(self, py_class):
        """
            Сохранение таблицы в БД
        :param py_class: класс, по которому будет выстроена бд
        :return: статус сохранения или контролируемая ошибка
        """
        need_fields: List[Tuple] = handler.convert_python_types_in_sqlite_types(attributes=tuple(vars(py_class).items()),
                                                                                object_=True)
        tables_list: tuple = self.get_tables()
        title_class: str = py_class.__name__.lower()
        if title_class not in tables_list:
            self._commit(queries=util.create_table(title=title_class,
                                                   attributes=need_fields))
            return TABLE_WAS_CREATED
        else:
            for table in tables_list:
                if set(row[1:] for row in self.get_table_info(table)) == set(need_fields):
                    raise Exception(EXCEPTION_TEXT_CLASS_EXIST)
            else:
                self._execute(sql_queries.DROP_TABLE(title_class))
                self._commit(queries=util.create_table(title=title_class,
                                                       attributes=need_fields))
                return TABLE_WAS_UPDATED

    def delete_object(self, py_object: object):
        """
            Удаление записи
        :param py_object: объект записи
        :return: статус удаления или контролируемая ошибка
        """
        need_fields: List[Tuple] = handler.convert_python_types_in_sqlite_types(attributes=tuple(vars(py_object).items()),
                                                                                object_=True)
        tables_list: tuple = self.get_tables()

        for table in tables_list:

            if set(row[1:] for row in self.get_table_info(table)) == set(need_fields):

                try:
                    self._execute(queries=util.check_having_in_table(table=table,
                                                                     id_=py_object.id))
                    id_: int = self._cursor.fetchone()[0]

                except AttributeError:
                    raise Exception(EXCEPTION_TEXT_NO_ID)
                except (IndexError, TypeError):
                    raise Exception(EXCEPTION_TEXT_NO_RECORD)

                self._commit(queries=util.delete_object(table=table,
                                                        row_id=id_))
                return RECORD_WAS_DELETED

        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS)

    def delete_class(self, py_class):
        """
            Удаление таблицы из БД
        :param py_class: класс, по которому будет удалена бд
        :return: статус удаления или контролируемая ошибка
        """
        need_fields: List[Tuple] = handler.convert_python_types_in_sqlite_types(attributes=tuple(vars(py_class).items()))
        tables_list: tuple = self.get_tables()
        title_class: str = py_class.__name__.lower()
        if title_class not in tables_list:
            raise Exception(EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS)
        else:
            for table in tables_list:
                if set(row[1:] for row in self.get_table_info(table)) == set(need_fields):
                    self._commit(queries=util.delete_class(table=table))
                    return TABLE_WAS_DELETED
            else:
                raise Exception(EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS)

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

    def _get_data_from_table(self, table: str, attributes: Union[list, tuple, None]) -> List[Tuple]:
        """
            Данный метод создан для уменьшения кол-ва кода, он:
                генерирует запрос на основе переданных параметров;
                получает данные о таблице по полям, а именно: айди поля, название, тип;
                соединяет поля с данными.
        :param table: название таблицы
        :param attributes: необходимые аттрибуты для поиска записей в бд
        :return: список кортежей структуры: названеи поля, его тип, его значение
        """
        query: str = util.generate_sql_to_find_object(table=table,
                                                      attributes=attributes)
        table_fields: List[Tuple] = self.get_table_info(table=table)
        self._execute(queries=query)
        return handler.merge_field_info_with_value(fields_info=table_fields,
                                                   data=self._cursor.fetchall())

    def find_object(self, table: str, py_object: object) -> list:
        """
            Поиск строки с эквивалетными параметрами что и у объекта
        :param table: название таблицы
        :param py_object: объект требуемый к нахождению
        :return: список кортежей где 1 кортеж является информацией о одном поле
        """
        if table in self.get_tables():
            return self._get_data_from_table(table=table, attributes=tuple(vars(py_object).items()))
        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE)

    def find_objects_by(self, table: str, *attributes):
        """
            Поиск записи по заданным параметрам
        :param table: название таблицы
        :param attributes: нужный параметры для поиска
        :return: найденные строки в формате: название стобца, тип, занчение
        """
        if table in self.get_tables():
            return self._get_data_from_table(table=table, attributes=tuple(attributes)[0])
        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE)

    def find_class(self, py_class):
        """
                    Поиск необходимого класса
                :param py_class: python класс
                :return: все данные найденого класса по ячейкам
                """
        need_fields: List[Tuple] = handler.convert_python_types_in_sqlite_types(attributes=tuple(vars(py_class).items()))
        tables_list: tuple = self.get_tables()
        for table in tables_list:
            if set(row[1:] for row in self.get_table_info(table)) == set(need_fields):
                return self._get_data_from_table(table=table, attributes=tuple())
        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS)

    def find_classes_by(self, *attributes):
        """
            Поиск необходимого класса по введенным аттрибутам
        :param py_class: python класс
        :return: все данные найденого класса по ячейкам
        """
        need_fields: List[Tuple] = handler.convert_python_types_in_sqlite_types(attributes=tuple(attributes)[0])
        tables_list: tuple = self.get_tables()
        for table in tables_list:
            if set(row[1:] for row in self.get_table_info(table)) == set(need_fields):
                return self._get_data_from_table(table=table, attributes=tuple())
        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS)

    def find_hierarches(self):
        """
            Поиск каких-либо иерархий, или же связанных таблиц
        :return: список кортежей с форматом: родительская таблица, дочерняя таблица.
        """
        tables_list: tuple = self.get_tables()
        relations: list = []

        for table in tables_list:
            query: str = sql_queries.GET_RELATIONS(table)

            self._execute(queries=query)

            if constraint := self._cursor.fetchone():
                parent_table: str = constraint[0]
                relations.append((parent_table, table))

        return relations

    def create_object(self, table: str, id_: Union[str, int]) -> object:
        """
            Создание объектов из одной записи
        :param table: название таблицы
        :param id_: запись в бд
        :return: список объектов
        """
        if table in self.get_tables():
            query: str = util.generate_sql_to_find_object(table=table,
                                                          attributes=(('id', id_),))
            self._execute(queries=query)
            if record := self._cursor.fetchone():
                return handler.serialize_to_py_object(title_columns=util.output_one_column(self._cursor.description),
                                                      data=[record])
            else:
                raise Exception(EXCEPTION_TEXT_NO_RECORD)

        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE)

    def create_objects(self, table: str, fid: Union[str, int], lid: Union[str, int]) -> List[object]:
        """
            Создание объектов из нескольки записей
        :param lid: правая граница множества
        :param fid: левая граница множества
        :param table: название таблицы
        :return: список объектов
        """
        if table in self.get_tables():
            query: str = util.generate_sql_to_find_object(table=table,
                                                          attributes=(('id', f' >= "{fid}'),
                                                                      ('id', f' <= "{lid}')))
            self._execute(queries=query)
            if record := self._cursor.fetchall():
                return handler.serialize_to_py_object(title_columns=util.output_one_column(self._cursor.description),
                                                      data=record)
            else:
                raise Exception(EXCEPTION_TEXT_NO_RECORD)

        else:
            raise Exception(EXCEPTION_TEXT_NO_TABLE)


def create_class(self, table: str, module: str):
    """
        Создание модуля
    :param table: название таблицы по которой создается модуль
    :param module: название модуля / класса в нём создаваемого
    :return:
    """
    if table.lower() in self.get_tables():
        handler.create_module(title_class=module,
                              class_=self.get_table_info(table))
    else:
        raise Exception(EXCEPTION_TEXT_NO_TABLE)


def main():
    print("Executing Py2SQL version %s." % __version__)
    with Database() as db:
        # print(db.get_table_info('asdasdasdasd'))
        # print(db.find_objects_by('car', (("color", "RED"), ("number", 5))))
        # print(db.find_object('car', Car()))
        print(db.find_class(Car))
        # print(db.get_table_info('asdasdasdasd'))
        # print(db.find_class(Car))
        # print(db.find_classes_by((('color', 'str'), ('number', 'int'), ('title', 'str'))))
        # print(db.find_hierarches())
        # db.create_object(Cat, '1')
        # db.create_objects('cat', 1, 2)
        # db.save_object(Car("BLACK", 20, 'RENO'))
        # db.save_object(Cat(22, 'test'))
        # db.save_class(Cat)
        # db.delete_object(Cat())
        # db.delete_class(py_class=Car)
        db.create_class('Cat', 'Cats')