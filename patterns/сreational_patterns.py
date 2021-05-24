import copy
import quopri
import sqlite3

from icecream import ic

from patterns.architectural_system_pattern_unit_of_work import DomainObject
# from patterns.behavioral_patterns import Subject
from veil_framework.log.log_config import log_config


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self, subject):
        for item in self.observers:
            item.update(subject)


class User(DomainObject):

    def __init__(self, id='', name='name', password='123'):
        self.id = id
        self.name = name
        self.password = password


class Teacher(User):
    def __init__(self, name):
        super().__init__(name=name)
        self.courses = []


class Student(User):
    def __init__(self, name='', password='123'):
        super().__init__(name=name, password=password)
        self.courses = []


class Methodist(User):
    def __init__(self, name):
        super().__init__(name=name)
        self.courses = []


class Admin(User):
    pass


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher,
        'methodist': Methodist,
        'admin': Admin
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        if type_ in cls.types:
            return cls.types[type_](name)
        else:
            raise TypeError(f'wrong user type {type_}')


# порождающий паттерн Прототип - Курс
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        self.teachers = []
        self.methodists = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify(student)

    def add_teacher(self, teacher: Teacher):
        self.teachers.append(teacher)
        teacher.courses.append(self)
        self.notify(teacher)

    def change_category(self, category):
        try:
            self.category.courses.remove(self)
        except Exception:
            pass
        self.category = category
        self.category.courses.append(self)


# Интерактивный курс
class InteractiveCourse(Course):
    pass


# Курс в записи
class RecordCourse(Course):
    pass


class WebinarCourse(Course):
    pass


class OfflineCourse(Course):
    pass


class Category(DomainObject):
    # auto_id = 0

    def __init__(self, id='', name='', parent_id=''):
        # self.id = Category.auto_id
        self.id = id
        # Category.auto_id += 1
        self.name = name
        self.parent_id = parent_id
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        # if self.category:
        #     result += self.category.course_count()
        return result


# порождающий паттерн Абстрактная фабрика - фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse,
        'webinar': WebinarCourse,
        'offline': OfflineCourse
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        if type_ in cls.types:
            return cls.types[type_](name, category)
        else:
            raise TypeError(f'wrong course type {type_}')


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name=name, parent_id=category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def find_elem_by_id(self, items: list, id: int):
        for item in items:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет элемента с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    def get_teacher(self, name) -> Teacher:
        for item in self.teachers:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs and 'name' in kwargs:
            name = kwargs['name']
        else:
            name = None

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, filename='', console=True):
        self.name = name
        self.filename = filename
        self.console = console
        self.logger = log_config(name, filename, console)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def exception(self, msg):
        self.logger.exception(msg)


CONNECTION = sqlite3.connect('patterns.sqlite')


class Mapper:

    def __init__(self, obj=None, cls=None, connection=CONNECTION):
        is_valid = False
        if not obj and not cls:
            raise DbClassTableException(f'unknown class for DB table')
        self.obj = obj
        self.cls = cls if cls else obj.__class__
        # ic(self.cls)
        for cls in self.cls.__mro__:
            if cls == DomainObject:
                is_valid = True
        if not is_valid:
            raise DbClassTableException(f'class {repr(self.cls)} not have parent class DomainObject')

        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = self.cls.__name__

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            self._create_obj(item)
            result.append(self.obj)
        return result

    def _is_valid(self, obj):
        if not obj.__class__ == self.cls:
            raise DbInsertException(f'object {obj} has wrong class for table {self.tablename}')

    def _create_obj(self, item):
        self.obj = self.cls()
        for el, key in zip(item, self._get_col_names_and_values()[0]):
            self.obj.__dict__[key] = el
        return self.obj

    def _get_col_names_and_values(self):
        res_name = []
        res_value = []
        for key, value in self.obj.__dict__.items():
            if not isinstance(value, (list, tuple, set)):
                res_name.append(key)
                res_value.append(value)
        return res_name, res_value

    def find_by_id(self, id):
        statement = f"SELECT * FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return self._create_obj(result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        self._is_valid(obj)
        self.obj = obj
        names, values = self._get_col_names_and_values()
        names_str = ''
        values_cnt = ''
        for el in names[1:]:
            names_str += el + ','
        names_str = names_str[:-1]
        for _ in values[1:]:
            values_cnt += '?,'
        values_cnt = values_cnt[:-1]
        statement = f"INSERT INTO {self.tablename} ({names_str}) VALUES ({values_cnt})"
        self.cursor.execute(statement, values[1:])
        ic(statement)
        ic(values[1:])
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        self._is_valid(obj)
        self.obj = obj
        names, values = self._get_col_names_and_values()
        names_str = ''
        for el in names[1:]:
            names_str += el + '=?, '
        names_str = names_str[:-2]
        values.append(values[0])
        values = values[1:]
        statement = f"UPDATE {self.tablename} SET {names_str} WHERE id=?"
        self.cursor.execute(statement, values)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        self._is_valid(obj)
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


# connection = sqlite3.connect('patterns.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'student': Mapper(cls=Student),
        'category': Mapper(cls=Category)
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, (Student, Category)):

            return Mapper(obj)
        #if isinstance(obj, Category):
            #return CategoryMapper(connection)

    @staticmethod
    def get_current_mapper(name: str):
        return MapperRegistry.mappers[name.lower()]


class DbClassTableException(Exception):
    def __init__(self, message):
        super().__init__(f'Class map to Db table error: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbInsertException(Exception):
    def __init__(self, message):
        super().__init__(f'Db insert error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
