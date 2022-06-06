import os

from django.conf import settings
from django.core.management.commands import startapp
from django.core.management.base import CommandError


class Command(startapp.Command):

    def handle(self, **options):
        """
        Overriding for directory management.

        Details:
            startapp generally takes in directory argument, which is fuzzy about
            existence of directory. So, by overriding this managemnet we take care of
            the making directory and proving the required path for apps.
        """

        app_name = options["name"]

        # Check Project hierarchy for how this works.
        directory = os.path.join(settings.PROJECT_ROOT, "apps", app_name)

        try:
            os.makedirs(directory)
        except FileExistsError:
            raise CommandError(f"{app_name} already exists!")

        options.update({"directory": directory})

        super().handle(**options)
