# -*- coding: utf8 -*-

from model import db, Student, Course
from api import get_arg, APIError
from flask import session


def add_course(fields):
    if 'role' not in session or not session['role'] == 'admin':
        raise APIError('Insufficient permission', status_code=403)

    course = Course()
    for key, value in fields:
        course.__setattr__(key, value)

    db.session.add(course)
    db.session.commit()
    return course.dict


def query_course_by_num(cid):
    course = Course.query.filter(Course.cid == cid).first()
    if course:
        return course.dict
    else:
        return {}


def query_course_by_id(id):
    course = Course.query.filter(Course.id == int(id)).first()
    if course:
        return course.dict
    else:
        return {}


def list_teacher_courses(teacher_id):
    courses = Course.query.filter(Course.teacher == int(teacher_id)).all()
    return [course for course in courses]


def list_course(search):
    page = int(get_arg(search, 'page', 1))
    limit = int(get_arg(search, 'limit', 20))
    keyword = get_arg(search, 'keyword', '')

    courses = Course.query.filter(Course.name.like('%%%s%%' % keyword))\
                    .offset(limit * (page - 1))\
                    .limit(limit)\
                    .all()

    return [course.dict for course in courses]


def update_course(id, fields):
    if 'role' not in session or not session['role'] == 'admin':
        raise APIError('Insufficient permission', status_code=403)

    course = Course.query.filter(Course.id == id).first()
    if not course:
        raise APIError('未找到指定的课程', status_code=404)

    for key, value in fields:
        course.__setattr__(key, value)

    db.session.commit()
    return course.dict


def delete_course(id):
    if 'role' not in session or not session['role'] == 'admin':
        raise APIError('Insufficient permission', status_code=403)

    course = Course.query.filter(Course.id == id).first()
    if not course:
        raise APIError('未找到指定的课程', status_code=404)

    db.session.delete(course)
    db.session.commit()
    return {'impact': 1}
