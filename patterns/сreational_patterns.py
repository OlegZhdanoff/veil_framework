import copy
import quopri

from veil_framework.log.log_config import log_config


class User:

    def __init__(self, login='', password=''):
        self.login = login
        self.password = password


class Teacher(User):
    pass


class Student(User):
    pass


class Methodist(User):
    pass


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
    def create(cls, type_):
        if type_ in cls.types:
            return cls.types[type_]()
        else:
            raise TypeError(f'wrong user type {type_}')


# порождающий паттерн Прототип - Курс
class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)

    def change_category(self, category):
        try:
            self.category.courses.remove(self)
        except Exception:
            pass
        self.category = category
        self.category.courses.append(self)
        # for i, course in enumerate(self.category.courses):
            # if course.name == self.name:
            #     lst = []
            #     lst.remove()
            #     self.category.courses.


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


# Категория
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
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
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

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

    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.logger = log_config(name, filename)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def exception(self, msg):
        self.logger.exception(msg)
