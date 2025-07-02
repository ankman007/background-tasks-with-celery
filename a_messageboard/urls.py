from django.urls import path
from a_messageboard.views import *

urlpatterns = [
    path('', home, name='home'),
    path('messageboard/<int:board_id>', messageboard_view, name='messageboard'),
    path('subscribe/', subscribe, name='subscribe'),
]