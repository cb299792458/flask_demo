from flask import Blueprint, render_template, redirect, url_for, request, abort, Response
import os
import psycopg2
import urllib.request
import json
from app.forms import AppointmentForm
from datetime import datetime, timedelta

CONNECTION_PARAMETERS = {
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASS"),
    "dbname": os.environ.get("DB_NAME"),
    "host": os.environ.get("DB_HOST"),
}       


bp=Blueprint('main',__name__,'/')

@bp.route('/', methods=['GET', 'POST'])
def main():
    d=datetime.now()
    return redirect(url_for(".daily", year=d.year, month=d.month, day=d.day))

@bp.route('/index')
def index():
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT *
                FROM appointments
                """
            )
            rows = curs.fetchall()
            print(rows)
    return render_template('index.html',rows=rows)

@bp.route('/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def daily(year,month,day):
    day=datetime(year=year,month=month,day=day)
    next_day=day+timedelta(days=1)


    form=AppointmentForm()
    if form.validate_on_submit():
        params = {
            'name': form.name.data,
            'start_datetime': datetime.combine(form.start_date.data, form.start_time.data),
            'end_datetime': datetime.combine(form.end_date.data, form.end_time.data),
            'description': form.description.data,
            'private': form.private.data
        }
        with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
            with conn.cursor() as curs:
                curs.execute(
                    """
                    INSERT INTO appointments (name, start_datetime, end_datetime, description, private)
                    VALUES (%(name)s, %(start_datetime)s, %(end_datetime)s, %(description)s, %(private)s);
                    """, params
                )
        return redirect('/')

    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                WHERE start_datetime BETWEEN %(day)s AND %(next_day)s
                ORDER BY start_datetime;
                """, {'day': day, 'next_day': next_day}
            )
            rows = curs.fetchall()

    return render_template('main.html',rows=rows,form=form)

@bp.route('/apt/<int:id>', methods=['GET'])
def show_weather(id):
    with psycopg2.connect(**CONNECTION_PARAMETERS) as conn:
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT id, name, start_datetime, end_datetime
                FROM appointments
                WHERE id = %(id)s
                """, {'id': id}
            )
            apt=curs.fetchone()

    date=apt[2].date()
    print(date)
    city='New%20York'
    
    source = urllib.request.urlopen(f'https://api.weatherapi.com/v1/history.json?key=8d0e3d06e20f473f8ba232426231407&q={city}&dt={date}').read()
    list_of_data = json.loads(source)
    forecast=list_of_data['forecast']['forecastday'][0]['day']
    print(forecast)

    if apt:
        return render_template('apt.html',apt=apt, forecast=forecast)
    else:
        return '<h1>Appointment not Found</h1>'