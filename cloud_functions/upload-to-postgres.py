import psycopg2
import pandas as pd
from io import StringIO
from datetime import datetime

now = datetime.now()
time_string = now.strftime("%d/%m/%Y_%H:%M:%S")


class Queries:
    """Queries class for different queries"""
    create_table = """ 
                   CREATE TABLE {table_name}(
                   );"""

    add_columns = """
                  ALTER TABLE {table_name}
                  ADD COLUMN {column} VARCHAR(100);"""


def format_columns(columns_list):
    """Formats column names from a csv file to ALPHANUMERIC characters
    symbols are excluded"""
    formatted_columns = []

    for column in columns_list:
        character_list = list([val for val in column if val.isalnum()])
        column = "".join(character_list)
        formatted_columns.append(column)

    return formatted_columns


def format_table_name(table_name):
    """Formats table name from a csv file to ALPHANUMERIC characters,
    symbols are excluded from the name"""
    table_character = list([val for val in table_name if val.isalnum()])
    table_name = "".join(table_character)
    return table_name


def upload_to_postgres(event, context):
    """
    Is triggered when an updated file is uploaded to a
    bucket-with-updated-files. Formats filename and columns to generate
    corresponding tablename and columns for PSQL. Creates a connection
    though psycopg2 library and copies data as a string from dataframe
    to database. Table names are partitioned by date.
    """
    conn = psycopg2.connect(
        host='/cloudsql/rd-month-project:europe-central2:updated-file-storage',
        database='postgres',
        user='postgres',
        password='abcabcabc')

    conn.autocommit = True
    cursor = conn.cursor()

    filename = event['name']

    df = pd.read_csv(f'gs://bucket-with-updated-files/{filename}')

    columns = format_columns(list(df.columns))

    table_name = format_table_name(filename + time_string)

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
