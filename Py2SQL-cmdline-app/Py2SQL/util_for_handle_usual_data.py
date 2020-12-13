from typing import *

import re

from config import SUPPORTED_TYPES

class Object(object):
    """
        Так как к чистому классу object нельзя добавлять новые аттрибуты
    """
    pass


def serialize_to_py_object(title_columns: list, data: List[Tuple]) -> List[object]:
    """
        Конвертируем данные из бд в объекты
    :param title_columns: список названий полей, или же классовых переменных
    :param data: ряды данных, или же сами объекты в будущем
    :return: список объектов
    """
    python_objects_list: List = []
    for row in data:
        new_object = Object()
        for field, value in zip(title_columns, row):
            print(field, value)
            object.__setattr__(new_object,
                               field,
                               value)
        python_objects_list.append(new_object)
    return python_objects_list


def merge_field_info_with_value(fields_info: List[Tuple], data: List[Tuple]) -> List[Tuple]:
    """
        Соединяем название и тип поля с его значением
    :param fields_info: список полей с кортежами в которых название и тип поля
    :param data: сами значения
    :return: список кортежей с названием поля, типом, и значением
    """
    result = []
    for row in data:
        for field, cell in zip(fields_info, row):
            result.append(field[1:] + (cell, ))
    return result

def convert_python_types_in_sqlite_types(class_: dict) -> List[Tuple]:
    """
        Вычленяем нужные поля, которые являются переменными, и их типы переводим в типы бд
    :param class_: нужный класс
    :return: список кортежей где каждый кортеж - имя поля, его тип.
    """
    result = []
    for title_var, attr in vars(class_).items():
        if not title_var.startswith('_'):
            type_in_db = re.search(pattern="\'[^\']*",
                                   string=str(attr)).group()[1:]
            result.append((title_var, SUPPORTED_TYPES.get(type_in_db)))
    return result
