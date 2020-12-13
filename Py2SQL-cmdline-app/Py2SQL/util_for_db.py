def output_one_column(data: list) -> tuple:
    return tuple(row[0] for row in data)


def table_info(title_columns: tuple, data: list) -> list:
    title_columns = tuple(row[0] for row in title_columns)
    return tuple((title_columns,) + tuple(data[0:]))
    return data