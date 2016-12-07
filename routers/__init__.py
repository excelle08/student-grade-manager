from flask import Flask, Response, redirect
from flask import session, request, jsonify, make_response
from model import db
from api import APIError
from api.user import is_logged_in
import json, re, os


app = Flask(__name__)
db.init_app(app)


def return_json(serializable):
    return Response(json.dumps(serializable), mimetype='application/json')


def serve_html(path):
    with open(path, 'r') as f:
        content = f.read()
    return Response(content, mimetype='text/html')


def get(url):
    return app.route(url, methods=['GET', 'POST'])


def post(url):
    return app.route(url, methods=['POST'])


def delete(url):
    return app.route(url, methods=['DELETE'])


def put(url):
    return app.route(url, methods=['PUT'])


@app.errorhandler(APIError)
def handle_api_error(error):
    response = jsonify(error=error.status_code, message=error.message, data='')
    response.status_code = error.status_code
    return response


@app.errorhandler(KeyError)
def handle_key_error(error):
    response = jsonify(error=400, message='Missing key %s' % str(error.message), data='')
    response.status_code = error.status_code
    return response


@app.before_request
def admin_interceptor():
    user = is_logged_in()
    if 'admin' in request.path:
        if not user:
            return redirect('/')
        if session['role'] != 'admin':
            return redirect('/')


@app.before_request
def html_interceptor():
    path = request.path
    if re.match(r'^\/.*\.html$', path):
        if not os.path.exists('html' + path):
            return Response('Requested file does not exist.', status=404)
        else:
            return serve_html('html' + path)


@get('/')
def hello():
    user = is_logged_in()
    if not user:
        return serve_html('html/login.html')
    if session['role'] == 'admin':
        return serve_html('html/admin.html')
    elif session['role'] == 'teacher':
        return serve_html('html/teacher.html')
    elif session['role'] == 'student':
        return serve_html('html/student.html')
    else:
        return 'Are you OK?'

