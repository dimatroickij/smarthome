from datetime import datetime

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from authentication.tokens import TokenGenerator
from smarthome.settings import SITE_PROTOCOL, SITE_URL


@shared_task
def sendEmailConfirm(userId):
    UserModel = get_user_model()
    user = UserModel.objects.get(pk=userId)
    mail_subject = 'Активация аккаунта на портале управления умным домом'
    message = render_to_string('registration/confirmEmail.html', {
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': TokenGenerator().make_token(user),
        'year': datetime.now(),
        'protocol': SITE_PROTOCOL,
        'url': SITE_URL
    })
    email = EmailMultiAlternatives(mail_subject, message, to=[user.email], )
    email.attach_alternative(message, 'text/html')
    email.content_subtype = 'html'
    email.send()
