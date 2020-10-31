from django.contrib.auth import get_user_model

from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.tasks import sendEmailConfirm


@receiver(post_save, sender=get_user_model())
def user_post_save(instance, created, *args, **kwargs):
    if created:
        sendEmailConfirm.delay(instance.pk)
