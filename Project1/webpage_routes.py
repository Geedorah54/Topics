#PURPOSE: Map basic webpage data routes to addressbar pages

from flask import Blueprint, render_template, request, redirect, url_for, session
from extract_data import fetch_data
from format_tables import render_homepage_table, render_visits_table
from extract_data import get_database_connection

# links current page to app.py start file
routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/home')
def display_homepage():
    rows = fetch_data("SELECT * FROM patients")
    table_html = render_homepage_table(rows)
    return render_template('homepage.html', table_html=table_html)

@routes_bp.route('/visits')
def display_visits():
    schedule = fetch_data("SELECT * FROM patients WHERE appointment_datetime IS NOT NULL")
    table_html = render_visits_table(schedule)
    return render_template('visits.html', table_html=table_html, schedule=schedule)

@routes_bp.route('/')
def login():
    msg = ''
    return render_template('login.html', msg=msg)

@routes_bp.route('/register')
def register():
    return render_template('register.html')

@routes_bp.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('routes.login'))