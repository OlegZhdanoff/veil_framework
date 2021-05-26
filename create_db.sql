
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS student;
CREATE TABLE student (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    password VARCHAR (32)
    );

DROP TABLE IF EXISTS Category;
CREATE TABLE Category (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    parent_id INTEGER
    );

DROP TABLE IF EXISTS Course;
CREATE TABLE Course (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32),
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES Category(id)
    );

DROP TABLE IF EXISTS student_course;
CREATE TABLE student_course (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    student_id INTEGER,
    category_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES student(id),
    FOREIGN KEY (category_id) REFERENCES Category(id)
    );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
