from fronts import date_front
from views import Index, About, Registration, Feedback

fronts = [date_front, ]

routes = {
    '/': Index(),
    '/about/': About(),
    '/registration/': Registration(),
    '/feedback/': Feedback(),
}
