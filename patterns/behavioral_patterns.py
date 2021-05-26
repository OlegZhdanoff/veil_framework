# import json_tricks
import jsonpickle
from icecream import ic

from patterns.сreational_patterns import MapperRegistry
from veil_framework.templator import render


# поведенческий паттерн - наблюдатель
# Курс
class Observer:

    def update(self, subject):
        pass


class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.name)


class EmailNotifier(Observer):

    def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        ic(self.obj)
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'
    context = {}
    mapper_type = 'default'
    mapper = None
    request = {}

    def get_context_data(self):
        return self.context

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        # if context and isinstance(context, dict):
        #     self.context = context
        # else:
        #     self.context = self.get_context_data()
        self.context = self.get_context_data()
        context = self.context if self.context else {}
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        self.mapper = MapperRegistry.get_current_mapper(self.mapper_type)
        self.request = request
        # ic(context)
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.mapper.all()

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        ic(context)
        return context


class CreateView(TemplateView):
    template_name = 'create.html'
    context = {}

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def add_context(self):
        pass

    def __call__(self, request: dict):
        self.context = request.get('request_params', self.context)
        self.add_context()
        ic(self.context)
        self.mapper = MapperRegistry.get_current_mapper(self.mapper_type)
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


class UpdateView(TemplateView):
    template_name = 'update.html'
    context = {}
    # mapper_type = 'default'
    # mapper = None

    @staticmethod
    def get_request_data(request):
        return request['data']

    def update_obj(self, data):
        pass

    def get_obj_by_id(self, id):
        pass

    def __call__(self, request):
        self.mapper = MapperRegistry.get_current_mapper(self.mapper_type)
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.update_obj(data)

            return self.render_template_with_context()
        else:
            request_params = request.get('request_params', None)
            if request_params:
                id = int(request_params['id'])
                self.get_obj_by_id(id)
                # category = site.find_category_by_id(int(request_params['id']))
                return super().__call__(self.context)
            else:
                return super().__call__(self.context)


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')

