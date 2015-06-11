#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/app_improved.py
# A payments application with basic security improvements added.

import info, uuid
from flask import (Flask, abort, flash, get_flashed_messages,
                   redirect, render_template, request, session, url_for)


app = Flask(__name__)
app.secret_key = 'saiGeij8AiS2ahleahMo5dahveixuV3J'

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if request.method == 'POST':
        if (username, password) in [('alfonzo', '123456'), ('sam', '123456'), ('may', '123456')]:
            session['username'] = username
            session['csrf_token'] = uuid.uuid4().hex
            return redirect(url_for('index'))
    return render_template('login.html', username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    infos = info.get_info_of(info.open_database(), username)
    return render_template('index.html', infos=infos, username=username,
                           flash_messages=get_flashed_messages())




@app.route('/change', methods=['GET', 'POST'])
def change():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))
    infos = info.get_info_of(info.open_database(), username)
    name = request.form.get('name', '').strip()
    age = request.form.get('age', '').strip()
    sex = request.form.get('sex', '').strip()
    email = request.form.get('email', '').strip()
    complaint = None
    if request.method == 'POST':
        if age and age.isdigit() and sex  and email:
            print (age, email, sex)
            info.update_info(info.open_database(), username, age, email, sex)
            flash('Change successful')
            return redirect(url_for('index'))
        complaint = ('Age and Sex must be an integer' if not age.isdigit() 
                     else 'Please fill in all fields')
    return render_template('change.html', infos=infos, complaint=complaint, name=name,
                           age=age, sex=sex, email = email, 
                           csrf_token=session['csrf_token'])

if __name__ == '__main__':
    app.debug = True
    app.run(host = "127.0.0.1", port = 5000, debug = True, threaded = True, ssl_context = 'adhoc')
