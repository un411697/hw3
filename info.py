#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter11/bank.py
# A small library of database routines to power a payments application.

import os, pprint, sqlite3
from collections import namedtuple

def open_database(path='info.db'):
    new = not os.path.exists(path)
    db = sqlite3.connect(path)
    if new:
        c = db.cursor()
        c.execute('CREATE TABLE test1 (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, email TEXT, work_id INTEGER, ssn TEXT, sex TEXT)')
        add_info(db, 'alfonzo', 21, 'alfonzo@nct.tw', 10141320, 'A123456789', 'M')
        add_info(db, 'sam', 22,  'hi124@gmail.com', 10156476, 'C123456789', 'M')
        add_info(db, 'may', 19,  'chang@wxa.cn', 10142103, 'B212345678', 'F')
        db.commit()

    return db

def add_info(db, name, age, email, work_id, ssn, sex):
    db.cursor().execute('INSERT INTO test1 (name, age, email, work_id, ssn, sex)'
                        ' VALUES (?, ?, ?, ?, ?, ?)', (name, age, email, work_id, ssn, sex))

def get_info_of(db, account):
    c = db.cursor()
    c.execute('SELECT name, age, email, work_id, ssn, sex FROM test1 where name = ? ', (account, ))
    Row = namedtuple('Row', [tup[0] for tup in c.description])
    return [Row(*row) for row in c.fetchall()]

def update_info(db, account, tmp_age, tmp_email, tmp_sex) :
    db.cursor().execute('UPDATE test1 SET age = ? , email = ? , sex = ? WHERE name = ? ', (tmp_age, tmp_email, tmp_sex, account ))
    db.commit()


if __name__ == '__main__':
    db = open_database()
    #pprint.pprint(get_info_of(db, 'alfonzo'))
