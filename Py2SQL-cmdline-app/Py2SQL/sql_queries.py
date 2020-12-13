GET_TABLES = """SELECT name 
                FROM sqlite_master
                WHERE type='table'
                ORDER BY name;"""

def get_table_info(table: str):
    return 'SELECT cid, ' \
           '       name,' \
           '       type ' \
           f'FROM pragma_table_info("{table}")'