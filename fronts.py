from datetime import date


# front controller
def date_front(request):
    request['date'] = date.today()
