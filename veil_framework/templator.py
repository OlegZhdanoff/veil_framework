from jinja2 import Template, Environment, FileSystemLoader

from veil_framework.settings import TEMPLATE_DIR, BASE_DIR


def render(template_name, folder=TEMPLATE_DIR, **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    file_path = BASE_DIR / folder / template_name
    if file_path.exists():
        # open template file
        with open(file_path, encoding='utf-8') as f:
            template_str = f.read()
        template = Environment(loader=FileSystemLoader(BASE_DIR / folder)).from_string(template_str)
        return template.render(**kwargs)
    else:
        return b'404 PAGE Not Found'
