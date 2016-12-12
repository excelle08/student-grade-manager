# -*- coding: utf8 -*-

from model import Student, Teacher, Course, Selection
from model import db
from api import get_arg, APIError
from api.user import query_user_by_id
from api.course import query_course_by_id
from sqlalchemy import or_


def create_selection(student_id, course_id):
    student = query_user_by_id('student', student_id)
    course = query_course_by_id(course_id)

    if not course:
        raise APIError(u'课程不存在', status_code=404)

    sel = Selection()
    sel.student = int(student_id)
    sel.course = int(course_id)
    sel.term = ''

    db.session.add(sel)
    db.session.commit()

    return sel.dict


def remove_selection(id):
    sel = Selection.query.filter(Selection.id == int(id)).first()
    if not sel:
        raise APIError('未找到指定选课信息', status_code=404)

    db.session.delete(sel)
    db.session.commit()

    return {"impact": 1}


def list_selections_of_course(search):
    course_id = int(get_arg(search, 'cid'))
    page = int(get_arg(search, 'page', 1))
    limit = int(get_arg(search, 'limit', 20))

    selections = Selection.query\
                        .filter(Selection.course == course_id)\
                        .offset((page - 1) * limit)\
                        .limit(limit)\
                        .all()

    return [sel.dict for sel in selections]


def list_selection_of_student(search):
    student_id = int(get_arg(search, 'sid'))
    page = int(get_arg(search, 'page', 1))
    limit = int(get_arg(search, 'limit', 10000))

    selections = Selection.query\
                        .filter(Selection.course == student_id)\
                        .offset((page - 1) * limit)\
                        .limit(limit)\
                        .all()

    return [sel.dict for sel in selections]


def list_selections(search):
    page = int(get_arg(search, 'page', 1))
    limit = int(get_arg(search, 'limit', 10000))
    keyword = get_arg(search, 'keyword', '')

    selections = Selection.query\
                        .offset((page - 1) * limit)\
                        .limit(limit)\
                        .all()

    if keyword == '':
        return [sel.dict for sel in selections]
    else:
        result = []
        for sel in selections:
            course = Course.query.filter(
                or_(
                    Course.name.like('%%%s%%' % keyword),
                    Course.cid.like('%%%s%%' % keyword)
                )
            ).first()
            student = Student.query.filter(
                or_(
                    Student.name.like('%%%s%%' % keyword),
                    Student.sid.like('%%%s%%' % keyword)
                )
            ).first()
            if course or student:
                result.append(sel.dict)
        return result


def query_selection(selection_id):
    sel = Selection.query.filter(Selection.id == int(selection_id)).first()
    if not sel:
        return {}
    else:
        return sel.dict


def get_student_courses(student_id):
    selections = list_selection_of_student({'sid': student_id, 'limit': 10000})
    courses = []
    for sel in selections:
        course = Course.query.filter(Course.id == sel['course']).first()
        courses.append(course.dict)
    return courses


def compute_gpa(score):
    if score < 60:
        return 0.0
    elif score >= 60 and score < 85:
        return 1.5 + (score - 60) * 0.1
    else:
        return 4.0


def write_grade(course_id, student_id, regular, midterm, final, total):
    sel = Selection.query.filter(
        Selection.course == int(course_id),
        Selection.student == int(student_id)
    ).first()

    if not sel:
        raise APIError('未找到相应的选课信息', status_code=404)
    try:
        sel.regular = int(regular)
        sel.mid_term = int(midterm)
        sel.final = int(final)
        sel.total = int(total)
        sel.GPA = compute_gpa(int(total))

        db.session.commit()
    except ValueError:
        raise APIError('请输入整数', status_code=500)

    return sel.dict


def write_rating(selection_id, rating):
    sel = Selection.query.filter(Selection.id == int(selection_id)).first()
    if not sel:
        raise APIError('未找到相应的选课信息', status_code=404)
    try:
        sel.rating = float(rating)

        db.session.commit()
    except ValueError:
        raise APIError('请输入数字', status_code=500)

    return sel.dict


def get_student_grades(student_id):
    result = []

    selections = list_selection_of_student({"sid": int(student_id), "limit": 10000})

    for sel in selections:
        course = Course.query.filter(Course.id == sel.course).first()
        if not course:
            continue

        result.append({
            'id': sel.id,
            'course_id': course.cid,
            'name': course.name,
            'teacher': course.teacher,
            'score': sel.total,
            'GPA': sel.GPA
        })
    return result

