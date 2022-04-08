import psycopg2
import pandas as pd
from io import StringIO
from datetime import datetime

now = datetime.now()
time_string = now.strftime("%d/%m/%Y_%H:%M:%S")


class Queries:
    create_table = """ 
                   CREATE TABLE {table_name}(
                   );"""

    add_columns = """
                  ALTER TABLE {table_name}
                  ADD COLUMN {column} VARCHAR(100);"""

    copy_from = """
                COPY {table_name}
                FROM {path}
                DELIMITER ','
                CSV HEADER;"""


def format_columns(columns_list):
    formatted_columns = []

    for column in columns_list:
        column = column.lower()
        column = column.replace(' ', '')
        formatted_columns.append(column)

    return formatted_columns


def upload_to_postgres(event, context):

    conn = psycopg2.connect(
        host='/cloudsql/crud-project-345807:europe-central2:sweeft-postgres',
        database='postgres',
        user='postgres',
        password='abcabcabc')

    conn.autocommit = True
    cursor = conn.cursor()

    filename = event['name']

    df = pd.read_csv(f'gs://updated-bucket/{filename}')

    columns = format_columns(list(df.columns))

    table_name = filename + time_string

    cursor.execute(Queries.create_table.format(
        table_name=table_name))

    for column in columns:
        cursor.execute(Queries.add_columns.format(
                       column=column, table_name=table_name))

    buffer = StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    try:
        cursor.copy_from(buffer, table_name, sep=",")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_stringio() done")
    cursor.close()
