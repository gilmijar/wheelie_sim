import mariadb as msc
from functools import lru_cache
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
    if expect_one:
        return cursor.fetchone()
    return cursor.fetchall()


def run_dml(sql):
    db, cursor = connection()
    cursor.execute(sql)
    db.commit()


def insert_dict(what, where, batch_size=500):
    sample = what[0]
    columns = tuple(sample.keys())
    placeholders = ', '.join(['?' for _ in sample])
    sql = f"INSERT INTO {where} ({', '.join(columns)}) VALUES ({placeholders})"
    db, cursor = connection()
    values = [tuple(row[key] for key in columns) for row in what]
    batches = [values[i:i+batch_size] for i in range(0, len(values), batch_size)]
    insert_count = 0
    insert_last_id = -1
    for i, batch in enumerate(batches):
        # print(f'\tRunning batch {i+1} of {len(batches)}, with {len(batch)} rows')
        cursor.executemany(sql, batch)
        insert_count += cursor.rowcount
        insert_last_id = cursor.lastrowid
        db.commit()
    return {'last_row_id': insert_last_id, 'rowcount': insert_count}