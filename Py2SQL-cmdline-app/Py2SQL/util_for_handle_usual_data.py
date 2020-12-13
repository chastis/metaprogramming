from typing import *


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


def merge_field_info_with_value(fields_info: List[Tuple], data: List[Tuple]):
    result = []
    for row in data:
        for field, cell in zip(fields_info, row):
            result.append(field[1:] + (cell, ))
    return result