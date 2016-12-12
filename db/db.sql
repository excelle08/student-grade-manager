-- noinspection SqlNoDataSourceInspectionForFile
-- port : '3306'
-- user : 'root'
-- password : 'password'
DROP DATABASE IF EXISTS grade_manager;
CREATE DATABASE grade_manager;
USE grade_manager;

CREATE TABLE admin(
id int PRIMARY KEY AUTO_INCREMENT,
username varchar(30) NOT NULL,
password varchar(32) NOT NULL
);

CREATE TABLE student(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
sid varchar(20) NOT NULL,
name varchar(30) NOT NULL,
gender INT NOT NULL,
password varchar(32) NOT NULL,
major varchar(100) NOT NULL
);

CREATE TABLE teacher(
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
tid varchar(20) NOT NULL,
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
id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
cid varchar(20) not null,
name varchar(30) NOT NULL,
teacher int NOT NULL,
place varchar(50) NOT NULL,
day int NOT NULL,
start_time int NOT NULL,
end_time int NOT NULL,
credit float NOT NULL
);

CREATE TABLE selection(
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
student INT NOT NULL,
course INT NOT NULL,
term INT NOT NULL,
regular float DEFAULT 0,
mid_term float DEFAULT 0,
final float DEFAULT 0,
total float DEFAULT 0,
GPA float DEFAULT 0,
rating float DEFAULT 0
);
