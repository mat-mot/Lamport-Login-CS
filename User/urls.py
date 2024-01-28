from django.urls import path

from User.views import signup, signin, repetitions, home

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='Signup'),
    path('signin/', signin, name='Signin'),
    path('', home, name='Home'),
    path('repetitions/', repetitions, name='Repetitions'),
]
