from django.urls import path
from a_messageboard.views import home, messageboard_detail, subscribe

urlpatterns = [
    path('', home, name='home'),
    path('messageboard/<int:board_id>/', messageboard_detail, name='messageboard_detail'),
    path('subscribe/<int:board_id>/', subscribe, name='subscribe'),
]