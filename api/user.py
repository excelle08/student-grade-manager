# -*- coding: utf-8 -*-

from model import Student, Teacher, Admin
from model import db
from api import APIError
from flask import session
import hashlib


def hash_password(plaintext):
    return hashlib.md5(plaintext).hexdigest()


def extract_user_credential(userobj):
    cred = {}
    if not userobj:
        return None

    try:
        cred['password'] = userobj.password
    except AttributeError:
        return None

    if isinstance(userobj, Student):
        cred['id'] = userobj.sid
        cred['username'] = userobj.sid
    elif isinstance(userobj, Teacher):
        cred['id'] = userobj.tid
        cred['username'] = userobj.tid
    elif isinstance(userobj, Admin):
        cred['id'] = userobj.uid
        cred['username'] = userobj.username

    return cred


def query_user(role, username, password):
    user_obj = None
    if role.lower() == 'student':
        user_obj = Student.query.filter(
            Student.sid == username,
            Student.password == hash_password(password)
        ).first()
    elif role.lower() == 'teacher':
        user_obj = Teacher.query.filter(
            Teacher.tid == username,
            Teacher.password == hash_password(password)
        ).first()
    elif role.lower() == 'admin':
        user_obj = Admin.query.filter(
            Admin.name == username,
            Admin.password == hash_password(password)
        ).first()

    return user_obj


def login(username, password, role):
    if username == '' or password == '' or role == '':
        raise APIError('请输入用户名,密码和登陆角色', status_code=400)

    userobj = query_user(role, username, password)

    if not userobj:
        raise APIError('请输入正确的用户名,密码与登陆角色', status_code=400)

    session['role'] = role
    creds = extract_user_credential(userobj)
    for k, v in creds.items():
        session[k] = v

    return userobj.dict


def logout():
    del session['id']
    del session['role']
    del session['username']
    del session['password']


def current_user():
    try:
        return query_user(session['role'],
                          session['username'],
                          session['password']
                          ).dict
    except KeyError:
        return {}


def is_logged_in():
    return current_user()


def admin_add_user(role, fields):
    if role.lower() == 'student':
        user = Student()
    elif role.lower() == 'teacher':
        user = Teacher()
    elif role.lower() == 'admin':
        user = Admin()
    else:
        raise APIError('Invalid role')

    fields['password'] = hash_password(fields['password'])
    for key, value in fields.items():
        if not value:
            continue
        user.__setattr__(key, value)

    db.session.add(user)
    db.session.commit()
    return user.dict

