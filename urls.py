from fronts import date_front
from views import Index, About, Registration


fronts = [date_front, ]

routes = {
    '/': Index(),
    '/about/': About(),
    '/registration/': Registration(),
}
