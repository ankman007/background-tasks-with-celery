from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class MessageBoard(models.Model):
    name = models.CharField(max_length=250, blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin_messageboards", null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now)
    subscribers = models.ManyToManyField(User, related_name='subscribed_messageboards', blank=True)

    def __str__(self):
        return self.name or f"MessageBoard {self.id}"


class Message(models.Model):
    messageboard = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="authored_messages")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.author.username}: {self.body[:30]}"
