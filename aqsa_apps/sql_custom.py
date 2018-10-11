# Author of Aqsa: Yulay Musin
from django.db import connection


def dict_fetch_all(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def sql(query, get_tuple=False):
    with connection.cursor() as cursor:
        cursor.execute(query)
        # row = cursor.fetchone()
        if get_tuple:
            return cursor.fetchall()
        else:
            return dict_fetch_all(cursor)
