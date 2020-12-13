DB_FILENAME = 'db.sqlite3'

SUPPORTED_TYPES = {'str': 'TEXT',
                   'int': 'INTEGER',
                   'float': 'REAL'}

EXCEPTION_TEXT_NO_TABLE = 'Введенной таблицы не найдено.'
EXCEPTION_TEXT_NO_TABLE_WITH_THESE_ATTRS = 'Таблицы с эквивалетными параметрами не найдено.'
EXCEPTION_TEXT_NO_RECORD = 'Запись с заданными параметрами не найдена.'