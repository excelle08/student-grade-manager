from routers import get, post, put, delete
from routers import return_json
from flask import request
from api.user import login, logout, current_user


@post('/api/user')
def user_login():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = login(username, password, role)
    return user


@get('/api/user')
def current_user():
    return current_user()


@delete('/api/user')
def user_logout():
    logout()
    return {'status': 1}
