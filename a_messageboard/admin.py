from django.contrib import admin
from .models import Message, MessageBoard

admin.site.register(MessageBoard)
admin.site.register(Message)
