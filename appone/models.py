# chat/models.py

from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    # беседа между двумя и более участниками
    members = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']

    def __str__(self):
        # выводим список участников
        return ", ".join([u.username for u in self.members.all()])


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    author       = models.ForeignKey(User, on_delete=models.CASCADE)
    content      = models.TextField()
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"
