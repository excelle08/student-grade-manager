# -*- coding: utf-8 -*-

from model import Student, Teacher, Admin
from model import db
from api import APIError, get_arg
from flask import session
from sqlalchemy import or_
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
        cred['id'] = userobj.id
        cred['username'] = userobj.username

    return cred


def query_user_by_cred(role, username, password_hash):
    user_obj = None
    if role.lower() == 'student':
        user_obj = Student.query.filter(
            Student.sid == username,
            Student.password == password_hash
        ).first()
    elif role.lower() == 'teacher':
        user_obj = Teacher.query.filter(
            Teacher.tid == username,
            Teacher.password == password_hash
        ).first()
    elif role.lower() == 'admin':
        user_obj = Admin.query.filter(
            Admin.username == username,
            Admin.password == password_hash
        ).first()

    return user_obj


def login(username, password, role):
    if username == '' or password == '' or role == '':
        raise APIError('请输入用户名,密码和登陆角色', status_code=400)

    userobj = query_user_by_cred(role, username, hash_password(password))

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
        print "Session: role=%s, username=%s, pwd=%s" % (
            session['role'], session['username'], session['password']
        )
        user = query_user_by_cred(session['role'],
                                  session['username'],
                                  session['password']
                                  )
        if user:
            return user.dict
        else:
            print 'User not found'
            return {}

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


def query_user_by_id(role, identifier, dict=True):
    if role.lower() == 'student':
        user = Student.query.filter(Student.sid == (identifier)).first()
    elif role.lower() == 'teacher':
        user = Teacher.query.filter(Teacher.tid == (identifier)).first()
    elif role.lower() == 'admin':
        user = Admin.query.filter(Admin.username == (identifier)).first()
    else:
        raise APIError('Invalid role')

    if not user:
        raise APIError('用户不存在', status_code=404)

    return user.dict if dict else user


def query_user_by_numid(role, id, dict=True):
    if role.lower() == 'student':
        user = Student.query.filter(Student.id == int(id)).first()
    elif role.lower() == 'teacher':
        user = Teacher.query.filter(Teacher.id == int(id)).first()
    elif role.lower() == 'admin':
        user = Admin.query.filter(Admin.id == int(id)).first()
    else:
        raise APIError('Invalid role')

    if not user:
        raise APIError('用户不存在', status_code=404)

    return user.dict if dict else user


def admin_edit_user(role, identifier, fields):
    user = query_user_by_id(role, identifier, False)

    if 'password' in fields and fields['password'].strip() != '':
        fields['password'] = hash_password(fields['password'])
    for key, value in fields.iteritems():
        print 'key=%s, val=%s' % (key, value)
        if not value:
            continue
        user.__setattr__(key, value)

    db.session.commit()
    return user.dict


def update_user(role, identifier, old_password, fields):
    user = query_user_by_cred(role, identifier, hash_password(old_password))
    if not user:
        raise APIError('原密码错误,不能修改用户信息!')

    return admin_edit_user(role, identifier, fields)


def admin_delete_user(role, identifier):
    user = query_user_by_id(role, identifier, False)

    db.session.delete(user)
    db.session.commit()
    return {'impact': 1}


def list_user(role, search):
    page = int(get_arg(search, 'page', 1))
    limit = int(get_arg(search, 'limit', 10))
    id_keyword = get_arg(search, 'keyword', '')

    if role == 'student':
        query = Student.query.filter(or_(Student.sid.like('%%%s%%' % id_keyword), Student.name.like('%%%s%%' % id_keyword)))
    elif role == 'teacher':
        query = Teacher.query.filter(or_(Teacher.tid.like('%%%s%%' % id_keyword), Teacher.name.like('%%%s%%' % id_keyword)))
    elif role == 'admin':
        query = Admin.query.filter(Admin.username.like('%%%s%%' % id_keyword))
    else:
        raise APIError('Invalid role')

    users = query.offset(limit * (page - 1)).limit(limit).all()
    return [user.dict for user in users]
