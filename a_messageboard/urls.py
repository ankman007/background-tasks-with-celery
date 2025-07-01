from django.urls import path
from a_messageboard.views import *

urlpatterns = [
    path('', messageboard_view, name='messageboard_view'),
]