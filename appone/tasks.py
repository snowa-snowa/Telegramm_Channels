from celery import shared_task
from django.core.mail import send_mail
from .models import Message


@shared_task
def send_reminder(reminder_id):
    reminder = Message.objects.get(pk=reminder_id)
    send_mail(
        reminder.subject,
        reminder.message,
        'your_email@example.com',
        [reminder.email]
    )
    reminder.sent = True
    reminder.save()
