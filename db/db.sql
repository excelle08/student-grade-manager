-- port : '3306'
-- user : 'root'
-- password : 'password'

CREATE DATABASE grade_manager;
USE grade_manager;

CREATE TABLE admin(
uid int PRIMARY KEY AUTO_INCREMENT,
username varchar(30) NOT NULL,
password varchar(32) NOT NULL
);

CREATE TABLE student(
sid INT NOT NULL PRIMARY KEY,
name varchar(30) NOT NULL,
gender INT NOT NULL,
password varchar(32) NOT NULL,
major varchar(100) NOT NULL
);

CREATE TABLE teacher(
tid INT NOT NULL PRIMARY KEY,
name varchar(30) NOT NULL,
gender int NOT NULL,
password varchar(32) NOT NULL,
title varchar(20),
address varchar(50),
telephone varchar(30),
email varchar(50),
intro text
);

CREATE TABLE course(
cid INT NOT NULL PRIMARY KEY,
name varchar(30) NOT NULL,
teacher int NOT NULL,
place varchar(50) NOT NULL,
day int NOT NULL,
start_time int NOT NULL,
end_time int NOT NULL,
credit float NOT NULL
);

CREATE TABLE selection(
id INT NOT NULL AUTO_INCREMENT,
student INT NOT NULL,
course NOT NULL,
term INT NOT NULL,
regular float DEFAULT 0,
mid_term float DEFAULT 0,
final float DEFAULT 0,
total float DEFAULT 0,
GPA float DEFAULT 0,
rating float DEFAULT 0,
PRIMARY KEY(student,course,term)
);
