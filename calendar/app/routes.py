from flask import Blueprint, render_template
import os
import psycopg2

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}       


bp=Blueprint('main',__name__,'/')

@bp.route('/')
def main():
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                ORDER BY start_datetime;
                """
            )
            rows = curs.fetchall()
            print(rows[0][1])
    return render_template('main.html',rows=rows)