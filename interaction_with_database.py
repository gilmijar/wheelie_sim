import mariadb as msc
from functools import lru_cache
from collections import namedtuple, Sequence
import config


@lru_cache(maxsize=1)
def connection():
    user = config.USER
    password = config.PASSWORD
    host = config.HOST
    port = config.PORT
    database = config.DATABASE
    mydb = msc.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = mydb.cursor(named_tuple=True)
    return mydb, cursor


def select_data(query, expect_one=False):
    db, cursor = connection()
    cursor.execute(query)
    data = cursor.fetchone() if expect_one else cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    return result_as_named_tuples(columns, data)


def result_as_named_tuples(cols, data, class_name='Result'):
    if not cols:
        raise ValueError('No column names provided')
    tuple_named = namedtuple(class_name, cols, rename=True)
    if not all(map(lambda x: isinstance(x, Sequence), data)):
        rows = tuple_named(*data)
    else:
        rows = [tuple_named(*row) for row in data]
    return rows


def run_dml(sql):
    db, cursor = connection()
    cursor.execute(sql)
    db.commit()


def insert_dict(what, where, batch_size=500):
    sample = what[0]
    columns = tuple(sample.keys())
    placeholders = ', '.join(['?' for _ in sample])
    sql = f"INSERT IGNORE INTO {where} ({', '.join(columns)}) VALUES ({placeholders})"
    db, cursor = connection()
    values = [tuple(row[key] for key in columns) for row in what]
    if len(values) == 1:
        cursor.execute(sql, values[0])
        db.commit()
    batches = [values[i:i+batch_size] for i in range(0, len(values), batch_size)]
    for i, batch in enumerate(batches):
        # print(f'\tRunning batch {i+1} of {len(batches)}, with {len(batch)} rows')
        cursor.executemany(sql, batch)
        db.commit()
