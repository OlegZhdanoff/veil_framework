from veil_framework.templator import render


class Index:
    def __call__(self, request):
        print(request.get('date', None))
        return '200 OK', render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'


class Registration:
    def __call__(self, request):
        return '200 OK', render('registration.html', date=request.get('date', None))


class Feedback:
    def __call__(self, request):
        return '200 OK', render('feedback.html', date=request.get('date', None))
