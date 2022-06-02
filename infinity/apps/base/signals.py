from django.dispatch import receiver
from django.contrib.auth import models
from django.db.utils import NotSupportedError
from django.db.models.signals import pre_save


@receiver(pre_save, sender=models.User)
def immutablize_model(*args, **kwargs):
    if kwargs.get("update_fields", set()) != {"last_login"}:
        raise NotSupportedError("User Model is Immutable")
