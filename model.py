from flask_sqlalchemy import SQLAlchemy
from api import Base

db = SQLAlchemy()


class Admin(db.Model, Base):
    __tablename__ = 'admin'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(30), nullable=False)
    password = db.Column('password', db.String(32), nullable=False)


class Student(db.Model, Base):
    __tablename__ = 'student'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True, autoincrement=True)
    sid = db.Column('sid', db.String(20), nullable=False)
    name = db.Column('name', db.String(30), nullable=False)
    gender = db.Column('gender', db.Integer, nullable=False)
    password = db.Column('password', db.String(32), nullable=False)
    major = db.Column('major', db.String(100), nullable=False)


class Teacher(db.Model, Base):
    __tablename__ = 'teacher'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True, autoincrement=True)
    tid = db.Column('tid', db.String(20), nullable=False)
    name = db.Column('name', db.String(30), nullable=False)
    gender = db.Column('gender', db.Integer, nullable=False)
    password = db.Column('password', db.String(32), nullable=False)
    title = db.Column('title', db.String(20))
    address = db.Column('address', db.String(50))
    telephone = db.Column('telephone', db.String(30))
    email = db.Column('email', db.String(50))
    intro = db.Column('intro', db.Text)


class Course(db.Model, Base):
    __tablename__ = 'course'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True, autoincrement=True)
    cid = db.Column('cid', db.String(20), nullable=False)
    name = db.Column('name', db.String(30), nullable=False)
    teacher = db.Column('teacher', db.Integer, nullable=False)
    place = db.Column('place', db.String(50), nullable=False)
    day = db.Column('day', db.Integer, nullable=False)
    start_time = db.Column('start_time', db.Integer, nullable=False)
    end_time = db.Column('end_time', db.Integer, nullable=False)
    credit = db.Column('credit', db.Float, nullable=False)


class Selection(db.Model, Base):
    __tablename__ = 'selection'
    id = db.Column('id', db.Integer, nullable=False, primary_key=True, autoincrement=True)
    student = db.Column('student', db.Integer, nullable=False)
    course = db.Column('course', db.Integer, nullable=False)
    term = db.Column('term', db.Integer, nullable=False)
    regular = db.Column('regular', db.Float, default=0)
    mid_term = db.Column('mid_term', db.Float, default=0)
    final = db.Column('final', db.Float, default=0)
    total = db.Column('total', db.Float, default=0)
    GPA = db.Column('GPA', db.Float, default=0)
    rating = db.Column('rating', db.Float, default=0)
