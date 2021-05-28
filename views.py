from icecream import ic
from datetime import date

from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.behavioral_patterns import BaseSerializer, ListView, CreateView, EmailNotifier, SmsNotifier, UpdateView
from veil_framework.templator import render
from patterns.сreational_patterns import Engine, Logger, MapperRegistry, Student, Mapper, Course, Category
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main', 'main.log', console=True)
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes = {}


@AppRoute(routes=routes, url='/')
class Index(ListView):
    template_name = 'index.html'
    mapper_type = 'category'


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/registration/')
class Registration:
    @Debug(name='Registration')
    def __call__(self, request):
        return '200 OK', render('registration.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/feedback/')
class Feedback:
    @Debug(name='Feedback')
    def __call__(self, request):
        return '200 OK', render('feedback.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=request.get('date', None))


@AppRoute(routes=routes, url='/courses-list/')
class CoursesListView(ListView):
    template_name = 'course_list.html'
    mapper_type = 'course'

    def get_queryset(self):
        category_id = int(self.request['request_params']['id'])
        return self.mapper.find_by_field('category_id', category_id)

    def get_context_data(self):
        context = super().get_context_data()
        category_id = int(self.request['request_params']['id'])
        context['id'] = category_id
        mapper = MapperRegistry.get_current_mapper('category')
        context['category_name'] = mapper.find_by_id(category_id).name
        return context


@AppRoute(routes=routes, url='/create-course/')
class CreateCourse(CreateView):
    template_name = 'create_course.html'
    mapper_type = 'course'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        category_id = data['id']
        new_obj = Course(name=name, category_id=category_id)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory(CreateView):
    template_name = 'create_category.html'
    mapper_type = 'category'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        # new_obj = site.create_category(name)
        new_obj = Category(name=name)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/category-list/')
class CategoryListView(ListView):
    template_name = 'category_list.html'
    mapper_type = 'category'


@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:

    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            item_id = int(request_params['item_id'])
            cat_id = int(request_params['cat_id'])
            cat_name = request_params['cat_name']
            mapper = MapperRegistry.get_current_mapper('course')
            old_course = mapper.find_by_id(item_id)
            new_name = f'copy_{old_course.name}'
            new_course = old_course.clone()
            new_course.name = new_name
            new_course.mark_new()
            UnitOfWork.get_current().commit()
            courses = mapper.find_by_field('category_id', cat_id)

            return '200 OK', render('course_list.html', objects_list=courses, category_name=cat_name,
                                    id=cat_id)

        except KeyError:
            return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    template_name = 'student_list.html'
    mapper_type = 'student'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'
    mapper_type = 'student'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        # ic(name)
        new_obj = Student(name=name)
        # site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/update-student/')
class StudentUpdateView(UpdateView):
    template_name = 'update_student.html'
    mapper_type = 'student'

    def update_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        password = data['password']
        password = site.decode_value(password)
        obj = self.context['item']
        obj.name = name
        obj.password = password
        ic(name, password)
        obj.mark_dirty()
        UnitOfWork.get_current().commit()

    def get_obj_by_id(self, id):
        obj = self.mapper.find_by_id(id)
        self.context = {'item': obj}


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
