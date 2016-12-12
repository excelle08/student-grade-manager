# -*- coding: utf-8 -*-

from routers import get, post, put, delete
from routers import return_json
from flask import request
from api.user import *
from api.course import *
from api.selection import *


@post('/api/user')
def user_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = login(username, password, role)
    return return_json(user)


@get('/api/user')
def get_current_user():
    return return_json(current_user())


@delete('/api/user')
def user_logout():
    logout()
    return return_json({'status': 1})


@get('/api/course/<cid>')
def api_get_course_by_cid(cid):
    return return_json(query_course_by_num(cid))


@get('/api/course/id/<id>')
def api_get_course_by_id(id):
    return return_json(query_course_by_id(id))


@post('/api/admin/user/<role>')
def api_admin_add_user(role):
    if not role in ['student', 'teacher', 'admin']:
        raise APIError('Invalid role', status_code=404)
    args = {}
    for k, v in request.form.items():
        args[k] = v
    return return_json(admin_add_user(role, args))


@get('/api/user/<role>/<id>')
def api_query_user(role, id):
    if 'role' not in session or session['role'] == 'student':
        raise APIError('Insufficient permission', status_code=403)
    if role not in ['student', 'teacher', 'admin']:
        raise APIError('Invalid role', status_code=404)

    return return_json(
        query_user_by_id(role, id)
    )


@get('/api/user/<role>/id/<int:id>')
def api_query_user_by_numid(role, id):
    if 'role' not in session or session['role'] == 'student':
        raise APIError('Insufficient permission', status_code=403)
    if role not in ['student', 'teacher', 'admin']:
        raise APIError('Invalid role', status_code=404)

    return return_json(
        query_user_by_numid(role, id)
    )


@post('/api/user/<role>/<id>')
def api_update_user_info(role, id):
    print request.data
    if 'role' in session and session['role'] == 'admin':
        return return_json(admin_edit_user(role, id, request.form))
    else:
        if not 'old_password' in request.form:
            raise APIError('请输入原密码后更新用户信息', status_code=403)
        args = {}
        for key, value in request.form.items():
            if key == 'old_password':
                continue
            args[key] = value

        return return_json(update_user(role, id, request.form['old_password'], args))


@get('/api/user/<role>')
def api_list_user(role):
    if 'role' not in session or session['role'] == 'student':
        raise APIError('Insufficient permission', status_code=403)
    if role not in ['student', 'teacher', 'admin']:
        raise APIError('Invalid role', status_code=404)

    search_credit = request.args
    return return_json(list_user(role, search_credit))


@delete('/api/admin/user/<role>/<id>')
def api_admin_remove_user(role, id):
    if role not in ['student', 'teacher', 'admin']:
        raise APIError('Invalid role', status_code=404)

    return return_json(admin_delete_user(role, id))


@post('/api/admin/course')
def api_admin_add_course():
    return return_json(add_course(request.form))


@get('/api/admin/course')
def api_admin_list_course():
    return return_json(list_course(request.args))


@post('/api/admin/course/<id>')
def api_admin_update_course(id):
    return return_json(update_course(id, request.form))


@delete('/api/admin/course/<int:id>')
def api_admin_delete_course(id):
    return return_json(delete_course(id))


@get('/api/student/<int:id>/grades')
def api_retrieve_student_grades(id):
    return return_json(get_student_grades(id))


@get('/api/student/<int:id>/courses')
def api_retrieve_student_courses(id):
    return return_json(get_student_courses(id))


@get('/api/teacher/<int:id>/courses')
def api_retrieve_teacher_courses(id):
    return return_json(list_teacher_courses(id))


@post('/api/teacher/grade/<record_id>')
def api_teacher_grading(record_id):
    regular = request.form['regular']
    midterm = request.form['midterm']
    final = request.form['final']
    total = request.form['total']

    return return_json(
        write_grade(record_id, regular, midterm, final, total)
    )


@post('/api/admin/selection')
def api_admin_add_selection():
    student_id = int(request.form['student'])
    course_id = int(request.form['course'])
    return return_json(
        create_selection(student_id, course_id)
    )


@get('/api/admin/selection')
def api_admin_list_selections():
    return return_json(
        list_selections(request.args)
    )


@post('/api/admin/selection/<int:id>')
def api_admin_update_selection(id):
    return return_json(update_selection(
        id,
        int(request.form['student']),
        int(request.form['course'])
    ));


@delete('/api/admin/selection/<int:id>')
def api_admin_delete_selection(id):
    return return_json(remove_selection(id))


@get('/api/selection/<int:id>')
def api_get_selection(id):
    return return_json(query_selection(id))


@get('/api/selection/course/<int:course_id>')
def api_list_selection_by_course(course_id):
    search = {}
    search['cid'] = course_id
    for k, v in request.args:
        search[k] = v
    return return_json(list_selections_of_course(search))


@get('/api/selection/student/<int:student_id>')
def api_list_selection_by_student(student_id):
    search = {}
    search['sid'] = student_id
    for k, v in request.args:
        search[k] = v
    return return_json(list_selection_of_student(search))


@post('/api/student/rate/<int:sel_id>/<int:rating>')
def api_student_write_rating(sel_id, rating):
    return return_json(write_rating(sel_id, rating))

