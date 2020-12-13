def output_one_column(data: list) -> tuple:
    """
            Вывод кортежа при запросе одной колонки из бд,
            (чтоб не было кортеж в кортеже)
        :param data:
        :return:
        """
    return tuple(row[0] for row in data)


def table_info(title_columns: tuple, data: list) -> list:
    # title_columns = tuple(row[0] for row in title_columns)
    # return tuple((title_columns,) + tuple(data[0:]))
    return data


def generate_sql_to_find_object(table: str, attributes: tuple):
    query: str = 'SELECT * ' \
                 f'FROM `{table}` ' \
                 f'WHERE '
    if not attributes:
        return query[:-6]
    else:
        for field, value in attributes:
            if '>' in value or '<' in value:
                query += f'{field} {value}" AND '
            else:
                query += f'{field} = "{value}" AND '
        return query[:-4]