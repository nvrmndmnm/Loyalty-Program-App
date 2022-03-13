from django.core.mail import send_mail

from Loyalty_Program_App.celery import app


@app.task(name='send_email')
def send_email_task(subject, message, from_email, recipient):
    send_mail(subject=subject,
              message=message,
              from_email=from_email,
              recipient_list=[recipient]
              )
    return 'Email sent.'
