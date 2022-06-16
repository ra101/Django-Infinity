"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mredisboard` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``redisboard.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``redisboard.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import os


os.environ.setdefault('DJANGO_CONFIGURATION', 'Settings')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infinity.settings.redis_board")


def main():

    import django
    from django.conf import settings
    from configurations.management import execute_from_command_line
    from decouple import config


    django.setup()

    from redisboard.models import RedisServer
    RedisServer.objects.get_or_create(label="main", url=settings.REDIS_URL)

    redis_board_domain = config('REDIS_BOARD_DOMAIN_URL', default='localhost:6479')


    if settings.DEBUG:
        execute_from_command_line(['django-admin', 'runserver', '--insecure', redis_board_domain])
    else:
        execute_from_command_line(['django-admin', 'runserver', '--insecure', '--noreload', redis_board_domain])


if __name__ == "__main__":
    main()
