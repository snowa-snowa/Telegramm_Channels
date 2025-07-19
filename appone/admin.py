from django.contrib import admin
from .models import Message, Conversation, Profile

admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(Profile)