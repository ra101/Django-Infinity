"""Command for creating super-user and guest-user"""
from decouple import config
from django.db.models import Q
from django.db.transaction import atomic
from django.contrib.auth import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Defines `initadmins` command that creates admin accounts"""

    @atomic()
    def handle(self, *args, **options):
        """
        - Truncates old Auth Data
        - Create a SuperUser and GuestUser with ReadOnly Ablities
        - GuestUser: user/pass :: admin/admin
        """

        self.tuncate_auth_models()

        self.create_super_user()

        self.create_guest_user()

    def tuncate_auth_models(self):
        """
        Truncates User and Group Tables
        """

        return models.User.objects.all().delete(), models.Group.objects.all().delete()

    def create_super_user(self):
        """
        Creates a Super User from .env
        """

        return models.User.objects.create_superuser(
            username=config("SU_USERNAME"),
            password=config("SU_PASSWORD"),
        )

    def create_guest_user(self):
        """
        Creates a Guest User with `admin` as username and password
        that can view all data but only change live_settings
        """

        guest_user = models.User.objects.create_user(
            username="admin", password="admin", is_staff=True
        )
        guest_user.groups.add(self.create_guest_group())
        guest_user.save()

        return guest_user

    def create_guest_group(self):
        """
        Creates Group that can view all data but only change live_settings
        """

        guest_group = models.Group.objects.create(name="Guest")
        guest_group.permissions.set(self.get_guests_permission_qs())
        guest_group.save()

        return guest_group

    def get_guests_permission_qs(self):
        """
        Creates QuerySet of Permission:
         - that can view all data
         - but only change live_settings
        """

        return models.Permission.objects.filter(
            Q(codename__startswith="view") | Q(content_type__model="config")
        )
